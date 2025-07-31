using Microsoft.EntityFrameworkCore;
using Oracle.ManagedDataAccess.Client;
using Oracle.ManagedDataAccess.Types;
using CompanyApp.UserManagement.Models;
using System.Data;

namespace CompanyApp.UserManagement.Services
{
    public class UserManagementService
    {
        private readonly ApplicationDbContext _context;
        private readonly IConfiguration _configuration;

        public UserManagementService(ApplicationDbContext context, IConfiguration configuration)
        {
            _context = context;
            _configuration = configuration;
        }

        private OracleConnection GetConnection()
        {
            return new OracleConnection(_configuration.GetConnectionString("DefaultConnection"));
        }

        public async Task<List<Dictionary<string, object>>> SearchUsersAsync(string searchTerm)
        {
            var results = new List<Dictionary<string, object>>();

            using var connection = GetConnection();
            await connection.OpenAsync();

            using var command = new OracleCommand("sp_search_users", connection)
            {
                CommandType = CommandType.StoredProcedure
            };

            command.Parameters.Add("p_search_term", OracleDbType.Varchar2).Value = searchTerm;
            command.Parameters.Add("p_cursor", OracleDbType.RefCursor).Direction = ParameterDirection.Output;

            try
            {
                await command.ExecuteNonQueryAsync();

                var refCursor = (OracleRefCursor)command.Parameters["p_cursor"].Value;
                using var reader = refCursor.GetDataReader();
                while (await reader.ReadAsync())
                {
                    var row = new Dictionary<string, object>();
                    for (int i = 0; i < reader.FieldCount; i++)
                    {
                        row[reader.GetName(i)] = reader.GetValue(i);
                    }
                    results.Add(row);
                }
            }
            catch (Exception ex)
            {
                results.Add(new Dictionary<string, object> { { "error", ex.Message } });
            }

            return results;
        }

        public async Task<List<Dictionary<string, object>>> GetUserOrdersAsync(string customerId)
        {
            var results = new List<Dictionary<string, object>>();

            using var connection = GetConnection();
            await connection.OpenAsync();

            using var command = new OracleCommand("sp_get_customer_orders", connection)
            {
                CommandType = CommandType.StoredProcedure
            };

            command.Parameters.Add("p_customer_id", OracleDbType.Varchar2).Value = customerId;
            command.Parameters.Add("p_cursor", OracleDbType.RefCursor).Direction = ParameterDirection.Output;

            try
            {
                await command.ExecuteNonQueryAsync();

                var refCursor = (OracleRefCursor)command.Parameters["p_cursor"].Value;
                using var reader = refCursor.GetDataReader();
                while (await reader.ReadAsync())
                {
                    var row = new Dictionary<string, object>();
                    for (int i = 0; i < reader.FieldCount; i++)
                    {
                        row[reader.GetName(i)] = reader.GetValue(i);
                    }
                    results.Add(row);
                }
            }
            catch (Exception ex)
            {
                results.Add(new Dictionary<string, object> { { "error", ex.Message } });
            }

            return results;
        }

        public async Task<Dictionary<string, object>> ValidateUserAccessAsync(string username, string accessLevel)
        {
            using var connection = GetConnection();
            await connection.OpenAsync();

            using var command = new OracleCommand("BEGIN :result := sp_validate_user_access(:username, :access_level); END;", connection);

            command.Parameters.Add("result", OracleDbType.Int32).Direction = ParameterDirection.Output;
            command.Parameters.Add("username", OracleDbType.Varchar2).Value = username;
            command.Parameters.Add("access_level", OracleDbType.Varchar2).Value = accessLevel;

            try
            {
                await command.ExecuteNonQueryAsync();
                var result = Convert.ToInt32(command.Parameters["result"].Value);
                
                return new Dictionary<string, object>
                {
                    { "hasAccess", result > 0 },
                    { "accessCount", result },
                    { "username", username },
                    { "requestedLevel", accessLevel }
                };
            }
            catch (Exception ex)
            {
                return new Dictionary<string, object>
                {
                    { "error", ex.Message },
                    { "hasAccess", false },
                    { "accessCount", -1 },
                    { "username", username }
                };
            }
        }

        public async Task<List<Dictionary<string, object>>> SearchUsersSecureAsync(string searchTerm)
        {
            var results = new List<Dictionary<string, object>>();

            using var connection = GetConnection();
            await connection.OpenAsync();

            using var command = new OracleCommand("sp_search_users_secure", connection)
            {
                CommandType = CommandType.StoredProcedure
            };

            command.Parameters.Add("p_search_term", OracleDbType.Varchar2).Value = searchTerm;
            command.Parameters.Add("p_cursor", OracleDbType.RefCursor).Direction = ParameterDirection.Output;

            try
            {
                await command.ExecuteNonQueryAsync();

                var refCursor = (OracleRefCursor)command.Parameters["p_cursor"].Value;
                using var reader = refCursor.GetDataReader();
                while (await reader.ReadAsync())
                {
                    var row = new Dictionary<string, object>();
                    for (int i = 0; i < reader.FieldCount; i++)
                    {
                        row[reader.GetName(i)] = reader.GetValue(i);
                    }
                    results.Add(row);
                }
            }
            catch (Exception)
            {
                results.Add(new Dictionary<string, object> { { "error", "An error occurred while processing your request" } });
            }

            return results;
        }

        public async Task<List<Dictionary<string, object>>> GetUserOrdersSecureAsync(string customerId)
        {
            var results = new List<Dictionary<string, object>>();

            using var connection = GetConnection();
            await connection.OpenAsync();

            using var command = new OracleCommand("sp_get_customer_orders_secure", connection)
            {
                CommandType = CommandType.StoredProcedure
            };

            if (!long.TryParse(customerId, out long customerIdLong))
            {
                results.Add(new Dictionary<string, object> { { "error", "Invalid customer ID format" } });
                return results;
            }

            command.Parameters.Add("p_customer_id", OracleDbType.Int64).Value = customerIdLong;
            command.Parameters.Add("p_cursor", OracleDbType.RefCursor).Direction = ParameterDirection.Output;

            try
            {
                await command.ExecuteNonQueryAsync();

                var refCursor = (OracleRefCursor)command.Parameters["p_cursor"].Value;
                using var reader = refCursor.GetDataReader();
                while (await reader.ReadAsync())
                {
                    var row = new Dictionary<string, object>();
                    for (int i = 0; i < reader.FieldCount; i++)
                    {
                        row[reader.GetName(i)] = reader.GetValue(i);
                    }
                    results.Add(row);
                }
            }
            catch (Exception)
            {
                results.Add(new Dictionary<string, object> { { "error", "An error occurred while processing your request" } });
            }

            return results;
        }
    }
}
