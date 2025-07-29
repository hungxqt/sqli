package sqli.servlets;

import java.io.IOException;
import java.sql.Connection;
import java.sql.ResultSet;
import java.sql.Statement;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import sqli.DatabaseUtil;

public class TimeServlet extends HttpServlet {
    
    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
            
        String name = request.getParameter("name");
        String result = "";
        String query = "";
        String error = "";
        
        if (name != null && !name.trim().isEmpty()) {
            query = "SELECT username FROM users WHERE username = '" + name + "'";
            
            long startTime = System.currentTimeMillis();
            
            try (Connection conn = DatabaseUtil.getConnection();
                 Statement stmt = conn.createStatement();
                 ResultSet rs = stmt.executeQuery(query)) {
                
                // Execute the query (result doesn't matter for time-based)
                
            } catch (Exception e) {
                // Suppress errors for time-based injection
            }
            
            long endTime = System.currentTimeMillis();
            result = "query executed";
        }
        
        request.setAttribute("searchTerm", name);
        request.setAttribute("result", result);
        request.setAttribute("query", query);
        request.setAttribute("error", error);
        
        request.getRequestDispatcher("/WEB-INF/views/time.jsp").forward(request, response);
    }
}
