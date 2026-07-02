import time
import concurrent.futures
import threading
from typing import Callable, List, Tuple, Dict, Any
from tqdm import tqdm

def execute_parallel(
        target_function: Callable,
        labeled_tasks: List[Tuple[str, Tuple]],
        max_workers: int = 4,
        max_retries: int = 2,
        show_individual_timings: bool = True
) -> Dict[str, Any]:
    """
    Executes a batch of tasks in parallel using a thread pool, with automatic retries for failures.
    
    Args:
        target_function: The target function to execute for each task in the batch.
        labeled_tasks: A list of tuples containing (task_identifier, arguments_tuple).
        max_workers: The maximum number of concurrent threads to deploy. Defaults to 4.
        max_retries: The number of times to re-attempt tasks that throw exceptions. Defaults to 2.
        show_individual_timings: If True, outputs the execution time of successful tasks. 
                                 Errors will print regardless of this flag. Defaults to True.

    Returns:
        A dictionary containing the successful results mapped by task_identifier, 
        detailed metrics per task, and the total execution duration.
        Format: { 
            'task_id': result_object, 
            'execution_metrics': dict, 
            '_total_batch_duration': float 
        }

    Raises:
        RuntimeError: If any tasks continue to fail after the max_retries limit is reached.
    """
    final_results = {}
    execution_metrics = {}
    batch_start_time = time.perf_counter()

    def execute_and_measure(task_id: str, task_args: Tuple) -> Tuple[str, Any, float, Exception]:
        task_start = time.perf_counter()
        try:
            result = target_function(*task_args)
            task_duration = time.perf_counter() - task_start
            return task_id, result, task_duration, None
        except Exception as execution_error:
            task_duration = time.perf_counter() - task_start
            return task_id, None, task_duration, execution_error

    def format_time_delta(seconds: float) -> str:
        hours, remainder = divmod(seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        
        if hours > 0:
            return f"{int(hours)} hr {int(minutes)} min {seconds:.2f} sec"
        elif minutes > 0:
            return f"{int(minutes)} min {seconds:.2f} sec"
        return f"{seconds:.2f} sec"

    def process_task_batch(current_batch: List[Tuple[str, Tuple]]):
        batch_results = {}
        batch_metrics = {}
        failed_batch_items = []

        batch_progress = tqdm(total=len(current_batch), desc="Executing Batch", position=0)
        progress_lock = threading.Lock()

        def tracked_task_execution(task_id, task_args):
            result_payload = execute_and_measure(task_id, task_args)
            with progress_lock:
                batch_progress.update(1)
            return result_payload

        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as thread_pool:
            future_to_task_map = {
                thread_pool.submit(tracked_task_execution, task_id, task_args): (task_id, task_args)
                for task_id, task_args in current_batch
            }

            for completed_future in concurrent.futures.as_completed(future_to_task_map):
                task_id, result, duration, error = completed_future.result()
                original_args = future_to_task_map[completed_future][1]
                
                batch_results[task_id] = result
                batch_metrics[task_id] = {
                    'duration': duration,
                    'status': 'error' if error else 'success',
                    'error': str(error) if error else None
                }
                if error:
                    failed_batch_items.append((task_id, original_args))

        batch_progress.close()
        return batch_results, batch_metrics, failed_batch_items

    # Initial Execution Phase
    primary_results, primary_metrics, pending_retries = process_task_batch(labeled_tasks)
    final_results.update(primary_results)
    execution_metrics.update(primary_metrics)

    # Retry Phase
    for attempt_number in range(1, max_retries + 1):
        if not pending_retries:
            break
        print(f"\nRetrying {len(pending_retries)} failed tasks (Attempt {attempt_number}/{max_retries})...")
        retry_results, retry_metrics, pending_retries = process_task_batch(pending_retries)
        final_results.update(retry_results)
        execution_metrics.update(retry_metrics)

    total_batch_duration = time.perf_counter() - batch_start_time

    # Console Summary
    print("\n" + "=" * 60)
    print("Execution Summary:")
    print(f"Total execution time: {format_time_delta(total_batch_duration)}")

    batch_contains_errors = any(metric['status'] == 'error' for metric in execution_metrics.values())

    if show_individual_timings or batch_contains_errors:
        print("\nIndividual Task Metrics:")

        sorted_metrics = sorted(
            execution_metrics.items(),
            key=lambda item: (0 if item[1]['status'] == 'success' else 1, item[1]['duration']),
            reverse=True
        )

        for task_id, metric_data in sorted_metrics:
            task_status = metric_data['status']
            task_duration = metric_data['duration']

            if task_status == 'error' or show_individual_timings:
                if task_status == 'success':
                    print(f"   - {task_id}: {format_time_delta(task_duration)} (SUCCESS)")
                else:
                    print(f"   - {task_id}: {format_time_delta(task_duration)} (Error: {metric_data['error']})")
                    
    print("=" * 60)
    
    if pending_retries:
        failed_task_ids = [t_id for t_id, _ in pending_retries]
        raise RuntimeError(f"Tasks strictly failed after {max_retries} retries: {failed_task_ids}")
        
    final_results['execution_metrics'] = execution_metrics
    final_results['_total_batch_duration'] = total_batch_duration
    return final_results
