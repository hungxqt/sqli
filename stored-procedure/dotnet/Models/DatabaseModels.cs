using Microsoft.EntityFrameworkCore;
using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace CompanyApp.UserManagement.Models
{
    [Table("users")]
    public class User
    {
        [Key]
        [Column("user_id")]
        public long UserId { get; set; }

        [Column("username")]
        [MaxLength(50)]
        public string Username { get; set; } = string.Empty;

        [Column("email")]
        [MaxLength(100)]
        public string Email { get; set; } = string.Empty;

        [Column("password")]
        public string Password { get; set; } = string.Empty;

        [Column("user_role")]
        [MaxLength(20)]
        public string UserRole { get; set; } = "user";

        [Column("department")]
        [MaxLength(50)]
        public string Department { get; set; } = "general";

        [Column("created_date")]
        public DateTime CreatedDate { get; set; }
    }

    [Table("orders")]
    public class Order
    {
        [Key]
        [Column("order_id")]
        public long OrderId { get; set; }

        [Column("customer_id")]
        public long CustomerId { get; set; }

        [Column("product_name")]
        [MaxLength(100)]
        public string ProductName { get; set; } = string.Empty;

        [Column("quantity")]
        public int Quantity { get; set; }

        [Column("unit_price")]
        [Precision(10, 2)]
        public decimal UnitPrice { get; set; }

        [Column("total_amount")]
        [Precision(10, 2)]
        public decimal TotalAmount { get; set; }

        [Column("order_date")]
        public DateTime OrderDate { get; set; }

        [Column("order_status")]
        [MaxLength(20)]
        public string OrderStatus { get; set; } = "pending";
    }

    [Table("user_sessions")]
    public class UserSession
    {
        [Key]
        [Column("session_id")]
        public long SessionId { get; set; }

        [Column("user_id")]
        public long UserId { get; set; }

        [Column("session_token")]
        [MaxLength(255)]
        public string SessionToken { get; set; } = string.Empty;

        [Column("access_level")]
        [MaxLength(50)]
        public string AccessLevel { get; set; } = string.Empty;

        [Column("created_at")]
        public DateTime CreatedAt { get; set; }

        [Column("expires_at")]
        public DateTime ExpiresAt { get; set; }
    }

    [Table("audit_log")]
    public class AuditLog
    {
        [Key]
        [Column("log_id")]
        public long LogId { get; set; }

        [Column("action_type")]
        [MaxLength(50)]
        public string ActionType { get; set; } = string.Empty;

        [Column("user_id")]
        public long? UserId { get; set; }

        [Column("details")]
        public string Details { get; set; } = string.Empty;

        [Column("timestamp")]
        public DateTime Timestamp { get; set; }
    }
}
