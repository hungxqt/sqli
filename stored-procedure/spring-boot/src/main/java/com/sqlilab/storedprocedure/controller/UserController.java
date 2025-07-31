package com.sqlilab.storedprocedure.controller;

import com.sqlilab.storedprocedure.service.UserManagementService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;

import java.util.List;
import java.util.Map;

@Controller
public class UserController {

    @Autowired
    private UserManagementService userService;

    @GetMapping("/")
    public String index(Model model) {
        return "index";
    }

    @GetMapping("/users")
    public String userSearch(Model model) {
        model.addAttribute("title", "User Search");
        model.addAttribute("description", "Search for users in the system by username or email.");
        return "users";
    }

    @PostMapping("/api/users/search")
    @ResponseBody
    public List<Map<String, Object>> searchUsers(@RequestParam String searchTerm) {
        return userService.searchUsers(searchTerm);
    }

    @GetMapping("/orders")
    public String orderManagement(Model model) {
        model.addAttribute("title", "Order Management");
        model.addAttribute("description", "View customer orders and order history.");
        return "orders";
    }

    @PostMapping("/api/orders/customer")
    @ResponseBody
    public List<Map<String, Object>> getCustomerOrders(@RequestParam String customerId) {
        return userService.getUserOrders(customerId);
    }

    @GetMapping("/access")
    public String accessControl(Model model) {
        model.addAttribute("title", "Access Validation");
        model.addAttribute("description", "Validate user access permissions and roles.");
        return "access";
    }

    @PostMapping("/api/access/validate")
    @ResponseBody
    public Map<String, Object> validateAccess(@RequestParam String username, @RequestParam String accessLevel) {
        return userService.validateUserAccess(username, accessLevel);
    }

    @GetMapping("/secure")
    public String secureExamples(Model model) {
        model.addAttribute("title", "Secure Implementation Examples");
        return "secure";
    }

    @PostMapping("/api/users/search-secure")
    @ResponseBody
    public List<Map<String, Object>> searchUsersSecure(@RequestParam String searchTerm) {
        return userService.searchUsersSecure(searchTerm);
    }

    @PostMapping("/api/orders/customer-secure")
    @ResponseBody
    public List<Map<String, Object>> getCustomerOrdersSecure(@RequestParam String customerId) {
        return userService.getUserOrdersSecure(customerId);
    }
}
