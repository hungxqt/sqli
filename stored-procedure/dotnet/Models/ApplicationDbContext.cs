using Microsoft.EntityFrameworkCore;

namespace CompanyApp.UserManagement.Models
{
    public class ApplicationDbContext : DbContext
    {
        public ApplicationDbContext(DbContextOptions<ApplicationDbContext> options) : base(options)
        {
        }

        public DbSet<User> Users { get; set; }
        public DbSet<Order> Orders { get; set; }
        public DbSet<UserSession> UserSessions { get; set; }
        public DbSet<AuditLog> AuditLogs { get; set; }

        protected override void OnModelCreating(ModelBuilder modelBuilder)
        {
            base.OnModelCreating(modelBuilder);

            modelBuilder.HasSequence("users_seq").StartsAt(1).IncrementsBy(1);
            modelBuilder.HasSequence("orders_seq").StartsAt(1).IncrementsBy(1);
            modelBuilder.HasSequence("sessions_seq").StartsAt(1).IncrementsBy(1);
            modelBuilder.HasSequence("audit_seq").StartsAt(1).IncrementsBy(1);

            modelBuilder.Entity<User>(entity =>
            {
                entity.Property(e => e.UserId).HasDefaultValueSql("users_seq.NEXTVAL");
                entity.Property(e => e.CreatedDate).HasDefaultValueSql("SYSDATE");
            });

            modelBuilder.Entity<Order>(entity =>
            {
                entity.Property(e => e.OrderId).HasDefaultValueSql("orders_seq.NEXTVAL");
                entity.Property(e => e.OrderDate).HasDefaultValueSql("SYSDATE");
            });

            modelBuilder.Entity<UserSession>(entity =>
            {
                entity.Property(e => e.SessionId).HasDefaultValueSql("sessions_seq.NEXTVAL");
                entity.Property(e => e.CreatedAt).HasDefaultValueSql("SYSDATE");
            });

            modelBuilder.Entity<AuditLog>(entity =>
            {
                entity.Property(e => e.LogId).HasDefaultValueSql("audit_seq.NEXTVAL");
                entity.Property(e => e.Timestamp).HasDefaultValueSql("SYSDATE");
            });
        }
    }
}
