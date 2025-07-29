using Microsoft.AspNetCore.Mvc;
using Microsoft.Data.Sqlite;
using dotnet.Models;
using System.Diagnostics;

namespace dotnet.Controllers
{
    public class SqliController : Controller
    {
        private readonly string _connectionString;

        public SqliController(IConfiguration configuration)
        {
            _connectionString = configuration.GetConnectionString("DefaultConnection") ?? 
                              "Data Source=sqli.db";
        }

        // Main index page
        public IActionResult Index()
        {
            return View();
        }

        // Lab 1: UNION-based SQL Injection
        public IActionResult Union(string? name)
        {
            ViewData["SearchTerm"] = name;
            ViewData["Users"] = new List<dynamic>();
            ViewData["Query"] = "";
            ViewData["Error"] = "";

            if (string.IsNullOrEmpty(name))
            {
                return View();
            }

            var query = $"SELECT id, username, password FROM Users WHERE username = '{name}'";
            ViewData["Query"] = query;

            try
            {
                using var connection = new SqliteConnection(_connectionString);
                connection.Open();
                using var command = new SqliteCommand(query, connection);
                using var reader = command.ExecuteReader();
                
                var users = new List<dynamic>();
                while (reader.Read())
                {
                    users.Add(new
                    {
                        Id = reader.GetInt32(0),
                        Username = reader.GetString(1),
                        Password = reader.GetString(2)
                    });
                }
                ViewData["Users"] = users;
            }
            catch (Exception ex)
            {
                ViewData["Error"] = ex.Message;
            }

            return View();
        }

        // Lab 2: Error/Reflect-based SQL Injection
        public IActionResult Reflect(string? name)
        {
            ViewData["SearchTerm"] = name;
            ViewData["Result"] = "";
            ViewData["Query"] = "";
            ViewData["Error"] = "";

            if (string.IsNullOrEmpty(name))
            {
                return View();
            }

            var query = $"SELECT username FROM Users WHERE username = '{name}' LIMIT 1";
            ViewData["Query"] = query;

            try
            {
                using var connection = new SqliteConnection(_connectionString);
                connection.Open();
                using var command = new SqliteCommand(query, connection);
                var result = command.ExecuteScalar();
                
                if (result != null)
                {
                    ViewData["Result"] = $"User '{result}' found!";
                }
                else
                {
                    ViewData["Result"] = $"User '{name}' not found.";
                }
            }
            catch (Exception ex)
            {
                ViewData["Error"] = ex.Message;
            }

            return View();
        }

        // Lab 3: Boolean-based Blind SQL Injection
        public IActionResult Boolean(string? name)
        {
            ViewData["SearchTerm"] = name;
            ViewData["Exists"] = (bool?)null;
            ViewData["Query"] = "";
            ViewData["Error"] = "";

            if (string.IsNullOrEmpty(name))
            {
                return View();
            }

            var query = $"SELECT COUNT(*) as count FROM Users WHERE username = '{name}'";
            ViewData["Query"] = query;

            try
            {
                using var connection = new SqliteConnection(_connectionString);
                connection.Open();
                using var command = new SqliteCommand(query, connection);
                var count = Convert.ToInt32(command.ExecuteScalar());
                ViewData["Exists"] = count > 0;
            }
            catch (Exception ex)
            {
                ViewData["Error"] = ex.Message;
            }

            return View();
        }

        // Lab 4: Time-based Blind SQL Injection
        public IActionResult Time(string? name)
        {
            ViewData["SearchTerm"] = name;
            ViewData["Result"] = "";
            ViewData["Query"] = "";
            ViewData["Error"] = "";

            if (string.IsNullOrEmpty(name))
            {
                return View();
            }

            var query = $"SELECT username FROM Users WHERE username = '{name}'";
            ViewData["Query"] = query;

            var stopwatch = Stopwatch.StartNew();
            
            try
            {
                using var connection = new SqliteConnection(_connectionString);
                connection.Open();
                using var command = new SqliteCommand(query, connection);
                command.ExecuteScalar();
            }
            catch (Exception)
            {
                // Suppress errors for time-based injection
            }
            
            stopwatch.Stop();
            ViewData["Result"] = "query executed";

            return View();
        }
    }
}
