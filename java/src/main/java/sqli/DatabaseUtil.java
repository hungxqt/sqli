package sqli;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;
import java.sql.Statement;

public class DatabaseUtil {
    private static final String DB_HOST = System.getenv("DB_HOST") != null ? System.getenv("DB_HOST") : "localhost";
    private static final String DB_PORT = System.getenv("DB_PORT") != null ? System.getenv("DB_PORT") : "3306";
    private static final String DB_DATABASE = System.getenv("DB_DATABASE") != null ? System.getenv("DB_DATABASE") : "tomcat";
    private static final String DB_USER = System.getenv("DB_USERNAME") != null ? System.getenv("DB_USERNAME") : "root";
    private static final String DB_PASSWORD = System.getenv("DB_PASSWORD") != null ? System.getenv("DB_PASSWORD") : "";
    
    private static final String DB_URL = "jdbc:mysql://" + DB_HOST + ":" + DB_PORT + "/" + DB_DATABASE + "?useSSL=false&allowPublicKeyRetrieval=true";
    private static final String DB_URL_NO_DB = "jdbc:mysql://" + DB_HOST + ":" + DB_PORT + "/?useSSL=false&allowPublicKeyRetrieval=true";
    
    static {
        try {
            Class.forName("com.mysql.cj.jdbc.Driver");
            initializeDatabase();
        } catch (ClassNotFoundException e) {
            e.printStackTrace();
        }
    }
    
    public static Connection getConnection() throws SQLException {
        return DriverManager.getConnection(DB_URL, DB_USER, DB_PASSWORD);
    }
    
    private static void initializeDatabase() {
        try (Connection conn = DriverManager.getConnection(DB_URL_NO_DB, DB_USER, DB_PASSWORD);
             Statement stmt = conn.createStatement()) {
            
            stmt.execute("CREATE DATABASE IF NOT EXISTS " + DB_DATABASE);
            stmt.execute("USE " + DB_DATABASE);
            
            String createTable = "CREATE TABLE IF NOT EXISTS users (" +
                "id INT AUTO_INCREMENT PRIMARY KEY, " +
                "username VARCHAR(255) NOT NULL, " +
                "password VARCHAR(255) NOT NULL, " +
                "created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP" +
                ")";
            stmt.execute(createTable);
            
            var rs = stmt.executeQuery("SELECT COUNT(*) FROM users");
            rs.next();
            if (rs.getInt(1) == 0) {
                String[] insertData = {
                    "INSERT INTO users (username, password) VALUES ('Dumb', 'Dumb')",
                    "INSERT INTO users (username, password) VALUES ('Angelina', 'I-kill-you')",
                    "INSERT INTO users (username, password) VALUES ('Dummy', 'p@ssword')",
                    "INSERT INTO users (username, password) VALUES ('secure', 'crappy')",
                    "INSERT INTO users (username, password) VALUES ('stupid', 'stupidity')",
                    "INSERT INTO users (username, password) VALUES ('superman', 'genious')",
                    "INSERT INTO users (username, password) VALUES ('batman', 'mob!le')",
                    "INSERT INTO users (username, password) VALUES ('admin', 'admin')"
                };
                
                for (String sql : insertData) {
                    stmt.execute(sql);
                }
            }
            
        } catch (SQLException e) {
            e.printStackTrace();
        }
    }
}
