package com.sqlilab.storedprocedure.service;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import javax.sql.DataSource;
import java.sql.*;
import java.util.*;

@Service
public class UserManagementService {

    @Autowired
    private DataSource dataSource;

    // User Search - Appears secure with parameterized calls
    // but the stored procedure concatenates strings internally
    public List<Map<String, Object>> searchUsers(String searchTerm) {
        List<Map<String, Object>> results = new ArrayList<>();
        
        try (Connection conn = dataSource.getConnection()) {
            // Application correctly uses parameterized call
            String sql = "{call sp_search_users(?, ?)}";
            CallableStatement stmt = conn.prepareCall(sql);
            stmt.setString(1, searchTerm);  // Parameterized input
            stmt.registerOutParameter(2, Types.REF_CURSOR);
            
            stmt.execute();
            
            ResultSet rs = (ResultSet) stmt.getObject(2);
            while (rs.next()) {
                Map<String, Object> row = new HashMap<>();
                row.put("id", rs.getLong("user_id"));
                row.put("username", rs.getString("username"));
                row.put("email", rs.getString("email"));
                row.put("role", rs.getString("user_role"));
                row.put("department", rs.getString("department"));
                results.add(row);
            }
            
        } catch (SQLException e) {
            Map<String, Object> error = new HashMap<>();
            error.put("error", e.getMessage());
            results.add(error);
        }
        
        return results;
    }

    // Order Management - Parameterized at application level
    // but procedure uses dynamic SQL construction
    public List<Map<String, Object>> getUserOrders(String customerId) {
        List<Map<String, Object>> results = new ArrayList<>();
        
        try (Connection conn = dataSource.getConnection()) {
            // Application correctly uses parameterized call
            String sql = "{call sp_get_customer_orders(?, ?)}";
            CallableStatement stmt = conn.prepareCall(sql);
            stmt.setString(1, customerId);  // Parameterized input
            stmt.registerOutParameter(2, Types.REF_CURSOR);
            
            stmt.execute();
            
            ResultSet rs = (ResultSet) stmt.getObject(2);
            while (rs.next()) {
                Map<String, Object> row = new HashMap<>();
                row.put("order_id", rs.getLong("order_id"));
                row.put("product_name", rs.getString("product_name"));
                row.put("quantity", rs.getInt("quantity"));
                row.put("unit_price", rs.getBigDecimal("unit_price"));
                row.put("total_amount", rs.getBigDecimal("total_amount"));
                row.put("order_date", rs.getTimestamp("order_date"));
                row.put("status", rs.getString("order_status"));
                results.add(row);
            }
            
        } catch (SQLException e) {
            Map<String, Object> error = new HashMap<>();
            error.put("error", e.getMessage());
            results.add(error);
        }
        
        return results;
    }

    // Authentication Check - Appears to use safe parameter binding
    // but procedure has vulnerable conditional logic
    public Map<String, Object> validateUserAccess(String username, String accessLevel) {
        try (Connection conn = dataSource.getConnection()) {
            // Application correctly uses parameterized call
            String sql = "{? = call sp_validate_user_access(?, ?)}";
            CallableStatement stmt = conn.prepareCall(sql);
            stmt.registerOutParameter(1, Types.NUMERIC);
            stmt.setString(2, username);     // Parameterized input
            stmt.setString(3, accessLevel);  // Parameterized input - but vulnerable in procedure
            
            stmt.execute();
            
            int result = stmt.getInt(1);
            return Map.of(
                "hasAccess", result > 0, 
                "accessCount", result,
                "username", username,
                "requestedLevel", accessLevel
            );
            
        } catch (SQLException e) {
            return Map.of(
                "error", e.getMessage(), 
                "hasAccess", false, 
                "accessCount", -1,
                "username", username
            );
        }
    }

    // Secure implementations for comparison
    public List<Map<String, Object>> searchUsersSecure(String searchTerm) {
        List<Map<String, Object>> results = new ArrayList<>();
        
        try (Connection conn = dataSource.getConnection()) {
            String sql = "{call sp_search_users_secure(?, ?)}";
            CallableStatement stmt = conn.prepareCall(sql);
            stmt.setString(1, searchTerm);
            stmt.registerOutParameter(2, Types.REF_CURSOR);
            
            stmt.execute();
            
            ResultSet rs = (ResultSet) stmt.getObject(2);
            while (rs.next()) {
                Map<String, Object> row = new HashMap<>();
                row.put("id", rs.getLong("user_id"));
                row.put("username", rs.getString("username"));
                row.put("email", rs.getString("email"));
                row.put("role", rs.getString("user_role"));
                row.put("department", rs.getString("department"));
                results.add(row);
            }
            
        } catch (SQLException e) {
            Map<String, Object> error = new HashMap<>();
            error.put("error", "An error occurred while processing your request");
            results.add(error);
        }
        
        return results;
    }

    public List<Map<String, Object>> getUserOrdersSecure(String customerId) {
        List<Map<String, Object>> results = new ArrayList<>();
        
        try (Connection conn = dataSource.getConnection()) {
            String sql = "{call sp_get_customer_orders_secure(?, ?)}";
            CallableStatement stmt = conn.prepareCall(sql);
            stmt.setLong(1, Long.parseLong(customerId));  // Proper numeric parameter
            stmt.registerOutParameter(2, Types.REF_CURSOR);
            
            stmt.execute();
            
            ResultSet rs = (ResultSet) stmt.getObject(2);
            while (rs.next()) {
                Map<String, Object> row = new HashMap<>();
                row.put("order_id", rs.getLong("order_id"));
                row.put("product_name", rs.getString("product_name"));
                row.put("quantity", rs.getInt("quantity"));
                row.put("unit_price", rs.getBigDecimal("unit_price"));
                row.put("total_amount", rs.getBigDecimal("total_amount"));
                row.put("order_date", rs.getTimestamp("order_date"));
                row.put("status", rs.getString("order_status"));
                results.add(row);
            }
            
        } catch (SQLException e) {
            Map<String, Object> error = new HashMap<>();
            error.put("error", "An error occurred while processing your request");
            results.add(error);
        }
        
        return results;
    }
}
