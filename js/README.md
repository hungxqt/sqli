# SQLi Labs - Node.js/Express Implementation

This is the JavaScript/Node.js version of the SQL injection labs, featuring the same functionality as the PHP, Python, .NET, and Java implementations.

## 🚀 Quick Start

### Prerequisites
- Node.js (v14 or higher)
- MySQL Server
- npm or yarn

### Installation

1. **Install dependencies:**
   ```bash
   npm install
   ```

2. **Configure database:**
   - Ensure MySQL is running on localhost:3306
   - Default credentials: username=`root`, password=`root`
   - Database will be auto-created on first run

3. **Start the application:**
   ```bash
   npm start
   ```
   
   Or for development with auto-reload:
   ```bash
   npm run dev
   ```

4. **Access the labs:**
   - Homepage: `http://localhost:3000/`
   - UNION Lab: `http://localhost:3000/union`
   - Reflect Lab: `http://localhost:3000/reflect`
   - Boolean Lab: `http://localhost:3000/boolean`
   - Time Lab: `http://localhost:3000/time`

## 🧪 Testing SQL Injections

### UNION-based SQLi
- URL: `/union?name=admin' UNION SELECT 1,username,email FROM users--`
- Shows multiple columns and allows data extraction

### Error/Reflect-based SQLi
- URL: `/reflect?name=admin'`
- Displays database errors for information gathering

### Boolean-based Blind SQLi
- URL: `/boolean?name=admin' AND 1=1--` (True condition)
- URL: `/boolean?name=admin' AND 1=2--` (False condition)
- Shows different responses for true/false conditions

### Time-based Blind SQLi
- URL: `/time?name=admin' AND SLEEP(5)--`
- Includes execution timing information

## 🔧 Configuration

You can modify database settings in `app.js`:

```javascript
const dbConfig = {
    host: 'localhost',
    user: 'root',
    password: 'root',
    database: 'security'
};
```

## 📦 Dependencies

- **express**: Web framework
- **mysql2**: MySQL database driver
- **ejs**: Template engine for views
- **nodemon**: Development auto-reload (dev dependency)

## 🛡️ Security Notice

This application is intentionally vulnerable for educational purposes. Do not deploy in production environments.
