package sqli.servlets;

import java.io.IOException;
import java.sql.Connection;
import java.sql.ResultSet;
import java.sql.Statement;
import java.util.ArrayList;
import java.util.List;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import sqli.DatabaseUtil;
import sqli.User;

public class UnionServlet extends HttpServlet {
    
    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
            
        String name = request.getParameter("name");
        List<User> users = new ArrayList<>();
        String query = "";
        String error = "";
        
        if (name != null && !name.trim().isEmpty()) {
            query = "SELECT id, username, password FROM users WHERE username = '" + name + "'";
            
            try (Connection conn = DatabaseUtil.getConnection();
                 Statement stmt = conn.createStatement();
                 ResultSet rs = stmt.executeQuery(query)) {
                
                while (rs.next()) {
                    User user = new User();
                    user.setId(rs.getInt("id"));
                    user.setUsername(rs.getString("username"));
                    user.setPassword(rs.getString("password"));
                    users.add(user);
                }
                
            } catch (Exception e) {
                error = e.getMessage();
            }
        }
        
        request.setAttribute("searchTerm", name);
        request.setAttribute("users", users);
        request.setAttribute("query", query);
        request.setAttribute("error", error);
        
        request.getRequestDispatcher("/WEB-INF/views/union.jsp").forward(request, response);
    }
}
