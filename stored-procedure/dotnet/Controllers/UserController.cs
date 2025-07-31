using Microsoft.AspNetCore.Mvc;
using CompanyApp.UserManagement.Services;

namespace CompanyApp.UserManagement.Controllers
{
    [ApiController]
    [Route("api")]
    public class UserController : ControllerBase
    {
        private readonly UserManagementService _userService;

        public UserController(UserManagementService userService)
        {
            _userService = userService;
        }

        [HttpPost("users/search")]
        public async Task<IActionResult> SearchUsers([FromForm] string searchTerm)
        {
            try
            {
                var results = await _userService.SearchUsersAsync(searchTerm);
                return Ok(results);
            }
            catch (Exception ex)
            {
                return BadRequest(new { error = ex.Message });
            }
        }

        [HttpPost("orders/customer")]
        public async Task<IActionResult> GetCustomerOrders([FromForm] string customerId)
        {
            try
            {
                var results = await _userService.GetUserOrdersAsync(customerId);
                return Ok(results);
            }
            catch (Exception ex)
            {
                return BadRequest(new { error = ex.Message });
            }
        }

        [HttpPost("access/validate")]
        public async Task<IActionResult> ValidateAccess([FromForm] string username, [FromForm] string accessLevel)
        {
            try
            {
                var result = await _userService.ValidateUserAccessAsync(username, accessLevel);
                return Ok(result);
            }
            catch (Exception ex)
            {
                return BadRequest(new { error = ex.Message });
            }
        }
        [HttpPost("users/search-secure")]
        public async Task<IActionResult> SearchUsersSecure([FromForm] string searchTerm)
        {
            try
            {
                var results = await _userService.SearchUsersSecureAsync(searchTerm);
                return Ok(results);
            }
            catch (Exception)
            {
                return BadRequest(new { error = "An error occurred while processing your request" });
            }
        }

        [HttpPost("orders/customer-secure")]
        public async Task<IActionResult> GetCustomerOrdersSecure([FromForm] string customerId)
        {
            try
            {
                var results = await _userService.GetUserOrdersSecureAsync(customerId);
                return Ok(results);
            }
            catch (Exception)
            {
                return BadRequest(new { error = "An error occurred while processing your request" });
            }
        }
    }
}
