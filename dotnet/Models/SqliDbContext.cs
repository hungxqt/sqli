using Microsoft.EntityFrameworkCore;

namespace dotnet.Models
{
    public class SqliDbContext : DbContext
    {
        public SqliDbContext(DbContextOptions<SqliDbContext> options) : base(options)
        {
        }

        public DbSet<User> Users { get; set; }

        protected override void OnModelCreating(ModelBuilder modelBuilder)
        {
            modelBuilder.Entity<User>(entity =>
            {
                entity.HasKey(e => e.Id);
                entity.Property(e => e.Username).IsRequired().HasMaxLength(255);
                entity.Property(e => e.Password).IsRequired().HasMaxLength(255);
                entity.Property(e => e.CreatedAt).IsRequired();
            });

            // Seed data
            modelBuilder.Entity<User>().HasData(
                new User { Id = 1, Username = "Dumb", Password = "Dumb", CreatedAt = DateTime.Now },
                new User { Id = 2, Username = "Angelina", Password = "I-kill-you", CreatedAt = DateTime.Now },
                new User { Id = 3, Username = "Dummy", Password = "p@ssword", CreatedAt = DateTime.Now },
                new User { Id = 4, Username = "secure", Password = "crappy", CreatedAt = DateTime.Now },
                new User { Id = 5, Username = "stupid", Password = "stupidity", CreatedAt = DateTime.Now },
                new User { Id = 6, Username = "superman", Password = "genious", CreatedAt = DateTime.Now },
                new User { Id = 7, Username = "batman", Password = "mob!le", CreatedAt = DateTime.Now },
                new User { Id = 8, Username = "admin", Password = "admin", CreatedAt = DateTime.Now }
            );
        }
    }
}
