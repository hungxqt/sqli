using Microsoft.EntityFrameworkCore;
using dotnet.Models;

var builder = WebApplication.CreateBuilder(args);

// Add services to the container.
builder.Services.AddControllersWithViews();

// Add MySQL database
builder.Services.AddDbContext<SqliDbContext>(options =>
    options.UseMySql(
        builder.Configuration.GetConnectionString("DefaultConnection") ?? 
        "Server=localhost;Database=sqli_labs;Uid=root;Pwd=;",
        ServerVersion.AutoDetect(builder.Configuration.GetConnectionString("DefaultConnection") ?? 
        "Server=localhost;Database=sqli_labs;Uid=root;Pwd=;")));

var app = builder.Build();

// Create database and seed data
using (var scope = app.Services.CreateScope())
{
    var context = scope.ServiceProvider.GetRequiredService<SqliDbContext>();
    context.Database.EnsureCreated();
}

app.UseRouting();
app.MapStaticAssets();

// SQLi Labs routes - match PHP structure
app.MapControllerRoute(
    name: "sqli_index",
    pattern: "/",
    defaults: new { controller = "Sqli", action = "Index" });

app.MapControllerRoute(
    name: "sqli_union",
    pattern: "/union",
    defaults: new { controller = "Sqli", action = "Union" });

app.MapControllerRoute(
    name: "sqli_reflect",
    pattern: "/reflect",
    defaults: new { controller = "Sqli", action = "Reflect" });

app.MapControllerRoute(
    name: "sqli_boolean",
    pattern: "/boolean",
    defaults: new { controller = "Sqli", action = "Boolean" });

app.MapControllerRoute(
    name: "sqli_time",
    pattern: "/time",
    defaults: new { controller = "Sqli", action = "Time" });

app.MapControllerRoute(
    name: "default",
    pattern: "{controller=Sqli}/{action=Index}/{id?}")
    .WithStaticAssets();

app.Run();
