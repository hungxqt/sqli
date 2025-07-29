package sqli.servlets;

import java.io.IOException;
import java.sql.Connection;
import java.sql.ResultSet;
import java.sql.Statement;
import javax.servlet.ServletException;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import sqli.DatabaseUtil;

public class BooleanServlet extends HttpServlet {
    
    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
            
        String name = request.getParameter("name");
        Boolean exists = null;
        String query = "";
        String error = "";
        
        if (name != null && !name.trim().isEmpty()) {
            query = "SELECT COUNT(*) as count FROM users WHERE username = '" + name + "'";
            
            try (Connection conn = DatabaseUtil.getConnection();
                 Statement stmt = conn.createStatement();
                 ResultSet rs = stmt.executeQuery(query)) {
                
                if (rs.next()) {
                    int count = rs.getInt("count");
                    exists = count > 0;
                }
                
            } catch (Exception e) {
                exists = false;
            }
        }
        
        request.setAttribute("searchTerm", name);
        request.setAttribute("exists", exists);
        request.setAttribute("query", query);
        request.setAttribute("error", error);
        
        request.getRequestDispatcher("/WEB-INF/views/boolean.jsp").forward(request, response);
    }
}
