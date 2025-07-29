package sqli.servlets;

import java.io.IOException;
import javax.servlet.ServletException;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

public class IndexServlet extends HttpServlet {
    
    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        
        System.out.println("IndexServlet: doGet method called");
        System.out.println("Request URI: " + request.getRequestURI());
        System.out.println("Context Path: " + request.getContextPath());
        
        try {
            request.getRequestDispatcher("/WEB-INF/views/index.jsp").forward(request, response);
            System.out.println("Successfully forwarded to index.jsp");
        } catch (Exception e) {
            System.out.println("Error forwarding to index.jsp: " + e.getMessage());
            e.printStackTrace();
            
            // Fallback: write directly to response
            response.setContentType("text/html");
            response.getWriter().println("<h1>SQLi Labs - IndexServlet Working!</h1>");
            response.getWriter().println("<p>There was an issue loading the JSP view.</p>");
            response.getWriter().println("<p><a href='union'>Union Lab</a></p>");
            response.getWriter().println("<p><a href='reflect'>Reflect Lab</a></p>");
            response.getWriter().println("<p><a href='boolean'>Boolean Lab</a></p>");
            response.getWriter().println("<p><a href='time'>Time Lab</a></p>");
        }
    }
}
