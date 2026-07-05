import logging
from typing import Dict, Any

# Configure standard logging instead of using print()
logger = logging.getLogger(__name__)

def execute_transactional_query(
    spark_session: Any, 
    sql_statement: str, 
    jdbc_connection_url: str, 
    credentials: Dict[str, str], 
    enable_logging: bool = True
) -> None:
    """
    Executes a transactional SQL statement directly against a database using PySpark's JVM JDBC gateway.
    
    Args:
        spark_session: The active SparkSession instance.
        sql_statement: The DDL or DML SQL query to execute (e.g., UPDATE, INSERT, DELETE).
        jdbc_connection_url: The JDBC URL for the target database.
        credentials: A dictionary containing 'user' and 'password' keys.
        enable_logging: If True, outputs the successful query to the system logger. Defaults to True.
        
    Raises:
        RuntimeError: If the database connection fails, the query syntax is invalid, 
                      or the transaction cannot be committed.
    """
    db_connection = None
    db_statement = None
    
    try:
        # 1. Establish Connection
        db_connection = spark_session._sc._gateway.jvm.java.sql.DriverManager.getConnection(
            jdbc_connection_url,
            credentials.get("user"),
            credentials.get("password")
        )
        
        # 2. Configure Transaction
        db_connection.setAutoCommit(False)
        db_statement = db_connection.createStatement()
        
        # 3. Execute and Commit
        db_statement.execute(sql_statement)
        db_connection.commit()
        
        if enable_logging:
            logger.info(f"Successfully executed JDBC query:\n{sql_statement}")
            
    except Exception as execution_error:
        # 4. Handle Rollback Safely
        if db_connection:
            try:
                db_connection.rollback()
                if enable_logging:
                    logger.warning("Transaction successfully rolled back after failure.")
            except Exception as rollback_error:
                logger.error(f"CRITICAL: Failed to rollback transaction: {rollback_error}")
        
        # 5. Surface the Error (Always)
        raise RuntimeError(f"JDBC SQL execution failed: {execution_error}") from execution_error
        
    finally:
        # 6. Resource Cleanup
        if db_statement:
            try:
                db_statement.close()
            except Exception:
                pass
        if db_connection:
            try:
                db_connection.close()
            except Exception:
                pass
