ALTER SESSION SET CONTAINER = XEPDB1;

CREATE USER sqli_lab IDENTIFIED BY "SqliLab123!";
GRANT CONNECT, RESOURCE, DBA TO sqli_lab;
ALTER USER sqli_lab QUOTA UNLIMITED ON USERS;

CONNECT sqli_lab/"SqliLab123!"@//localhost:1521/XEPDB1;

CREATE TABLE users (
    user_id NUMBER PRIMARY KEY,
    username VARCHAR2(50) NOT NULL,
    email VARCHAR2(100) NOT NULL,
    password VARCHAR2(255) NOT NULL,
    user_role VARCHAR2(20) DEFAULT 'user',
    department VARCHAR2(50) DEFAULT 'general',
    created_date DATE DEFAULT SYSDATE
);

CREATE TABLE orders (
    order_id NUMBER PRIMARY KEY,
    customer_id NUMBER REFERENCES users(user_id),
    product_name VARCHAR2(100) NOT NULL,
    quantity NUMBER NOT NULL,
    unit_price NUMBER(10,2) NOT NULL,
    total_amount NUMBER(10,2) NOT NULL,
    order_date DATE DEFAULT SYSDATE,
    order_status VARCHAR2(20) DEFAULT 'pending'
);

CREATE TABLE user_sessions (
    session_id NUMBER PRIMARY KEY,
    user_id NUMBER REFERENCES users(user_id),
    session_token VARCHAR2(255),
    access_level VARCHAR2(50),
    created_at DATE DEFAULT SYSDATE,
    expires_at DATE
);

CREATE TABLE audit_log (
    log_id NUMBER PRIMARY KEY,
    action_type VARCHAR2(50),
    user_id NUMBER,
    details CLOB,
    timestamp DATE DEFAULT SYSDATE
);

CREATE SEQUENCE users_seq START WITH 1 INCREMENT BY 1;
CREATE SEQUENCE orders_seq START WITH 1 INCREMENT BY 1;
CREATE SEQUENCE sessions_seq START WITH 1 INCREMENT BY 1;
CREATE SEQUENCE audit_seq START WITH 1 INCREMENT BY 1;

INSERT INTO users VALUES (users_seq.NEXTVAL, 'john_doe', 'john@company.com', 'password123', 'user', 'engineering', SYSDATE);
INSERT INTO users VALUES (users_seq.NEXTVAL, 'jane_smith', 'jane@company.com', 'secret456', 'manager', 'sales', SYSDATE);
INSERT INTO users VALUES (users_seq.NEXTVAL, 'admin_user', 'admin@company.com', 'admin789', 'admin', 'it', SYSDATE);
INSERT INTO users VALUES (users_seq.NEXTVAL, 'test_user', 'test@company.com', 'test123', 'user', 'qa', SYSDATE);
INSERT INTO users VALUES (users_seq.NEXTVAL, 'mary_johnson', 'mary@company.com', 'secure321', 'user', 'hr', SYSDATE);

INSERT INTO orders VALUES (orders_seq.NEXTVAL, 1, 'Laptop', 1, 999.99, 999.99, SYSDATE, 'completed');
INSERT INTO orders VALUES (orders_seq.NEXTVAL, 1, 'Mouse', 2, 25.50, 51.00, SYSDATE, 'pending');
INSERT INTO orders VALUES (orders_seq.NEXTVAL, 2, 'Keyboard', 1, 75.00, 75.00, SYSDATE, 'shipped');
INSERT INTO orders VALUES (orders_seq.NEXTVAL, 3, 'Monitor', 1, 299.99, 299.99, SYSDATE, 'completed');
INSERT INTO orders VALUES (orders_seq.NEXTVAL, 2, 'Webcam', 1, 89.99, 89.99, SYSDATE, 'processing');

INSERT INTO user_sessions VALUES (sessions_seq.NEXTVAL, 1, 'sess_abc123', 'standard', SYSDATE, SYSDATE + 1);
INSERT INTO user_sessions VALUES (sessions_seq.NEXTVAL, 3, 'sess_xyz789', 'admin', SYSDATE, SYSDATE + 1);

INSERT INTO audit_log VALUES (audit_seq.NEXTVAL, 'login', 1, 'User login successful', SYSDATE);
INSERT INTO audit_log VALUES (audit_seq.NEXTVAL, 'order_placed', 2, 'New order created', SYSDATE);

COMMIT;

CREATE OR REPLACE PROCEDURE sp_search_users(
    p_search_term IN VARCHAR2,
    p_cursor OUT SYS_REFCURSOR
) AS
    v_sql VARCHAR2(4000);
BEGIN
    v_sql := 'SELECT user_id, username, email, user_role, department FROM users WHERE username LIKE ''%' || p_search_term || '%'' OR email LIKE ''%' || p_search_term || '%''';
    
    OPEN p_cursor FOR v_sql;
    
    DBMS_OUTPUT.PUT_LINE('EXECUTED: ' || v_sql);
END;
/

CREATE OR REPLACE PROCEDURE sp_get_customer_orders(
    p_customer_id IN VARCHAR2, 
    p_cursor OUT SYS_REFCURSOR
) AS
    v_sql VARCHAR2(4000);
BEGIN
    v_sql := 'SELECT o.order_id, o.product_name, o.quantity, o.unit_price, o.total_amount, o.order_date, o.order_status, u.username 
              FROM orders o 
              JOIN users u ON o.customer_id = u.user_id 
              WHERE o.customer_id = ' || p_customer_id || ' ORDER BY o.order_date DESC';
    
    OPEN p_cursor FOR v_sql;
    
    DBMS_OUTPUT.PUT_LINE('EXECUTED: ' || v_sql);
END;
/

CREATE OR REPLACE FUNCTION sp_validate_user_access(
    p_username IN VARCHAR2,
    p_access_level IN VARCHAR2  
) RETURN NUMBER AS
    v_count NUMBER;
    v_sql VARCHAR2(4000);
BEGIN
    v_sql := 'SELECT COUNT(*) FROM users WHERE username = ''' || p_username || ''' ' || p_access_level;
    
    EXECUTE IMMEDIATE v_sql INTO v_count;
    
    DBMS_OUTPUT.PUT_LINE('EXECUTED: ' || v_sql);
    
    RETURN v_count;
EXCEPTION
    WHEN OTHERS THEN
        RETURN -1;
END;
/

CREATE OR REPLACE PROCEDURE sp_search_users_secure(
    p_search_term IN VARCHAR2,
    p_cursor OUT SYS_REFCURSOR
) AS
BEGIN
    OPEN p_cursor FOR
        SELECT user_id, username, email, user_role, department 
        FROM users 
        WHERE username LIKE '%' || p_search_term || '%' 
           OR email LIKE '%' || p_search_term || '%';
END;
/

CREATE OR REPLACE PROCEDURE sp_get_customer_orders_secure(
    p_customer_id IN NUMBER,  
    p_cursor OUT SYS_REFCURSOR
) AS
BEGIN
    OPEN p_cursor FOR
        SELECT o.order_id, o.product_name, o.quantity, o.unit_price, o.total_amount, o.order_date, o.order_status, u.username 
        FROM orders o 
        JOIN users u ON o.customer_id = u.user_id 
        WHERE o.customer_id = p_customer_id
        ORDER BY o.order_date DESC;
END;
/

CREATE OR REPLACE FUNCTION sp_validate_user_access_secure(
    p_username IN VARCHAR2,
    p_access_level IN VARCHAR2
) RETURN NUMBER AS
    v_count NUMBER;
BEGIN
    IF p_access_level NOT IN ('standard', 'admin', 'manager') THEN
        RETURN -1;
    END IF;
    
    SELECT COUNT(*) INTO v_count
    FROM users u
    JOIN user_sessions s ON u.user_id = s.user_id
    WHERE u.username = p_username 
      AND s.access_level = p_access_level
      AND s.expires_at > SYSDATE;
    
    RETURN v_count;
EXCEPTION
    WHEN OTHERS THEN
        RETURN -1;
END;
/

CREATE OR REPLACE VIEW user_summary AS
SELECT 
    u.username,
    u.email,
    u.user_role,
    u.department,
    COUNT(o.order_id) as order_count,
    NVL(SUM(o.total_amount), 0) as total_spent
FROM users u
LEFT JOIN orders o ON u.user_id = o.customer_id
GROUP BY u.username, u.email, u.user_role, u.department;

COMMIT;

GRANT EXECUTE ON sp_search_users TO PUBLIC;
GRANT EXECUTE ON sp_get_customer_orders TO PUBLIC;
GRANT EXECUTE ON sp_validate_user_access TO PUBLIC;
GRANT EXECUTE ON sp_search_users_secure TO PUBLIC;
GRANT EXECUTE ON sp_get_customer_orders_secure TO PUBLIC;
GRANT EXECUTE ON sp_validate_user_access_secure TO PUBLIC;

SET SERVEROUTPUT ON;

SELECT 'Database setup completed successfully!' FROM DUAL;
