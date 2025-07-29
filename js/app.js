const express = require('express');
const mysql = require('mysql2');
const path = require('path');

const app = express();
const PORT = process.env.PORT || 3000;

// Set EJS as template engine
app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, 'views'));

// Middleware
app.use(express.urlencoded({ extended: true }));
app.use(express.json());
app.use(express.static('public'));

// Database configuration
const dbConfig = {
    host: 'localhost',
    user: 'root',
    password: '',
    database: 'nodejs',
    multipleStatements: true
};

// Initialize database
async function initializeDatabase() {
    try {
        // Connect without database first
        const connection = mysql.createConnection({
            host: dbConfig.host,
            user: dbConfig.user,
            password: dbConfig.password,
            multipleStatements: true
        });

        // Create database and table if they don't exist
        const initSQL = `
            CREATE DATABASE IF NOT EXISTS nodejs;
            USE nodejs;
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(50) NOT NULL,
                password VARCHAR(100) NOT NULL
            );
            
            DELETE FROM users;
            ALTER TABLE users AUTO_INCREMENT = 1;
            
            INSERT INTO users (username, password) VALUES 
            ('Dumb', 'Dumb'),
            ('Angelina', 'I-kill-you'),
            ('Dummy', 'p@ssword'),
            ('secure', 'crappy'),
            ('stupid', 'stupidity'),
            ('superman', 'genious'),
            ('batman', 'mob!le'),
            ('admin', 'admin'),
            ('admin1', 'admin1'),
            ('admin2', 'admin2'),
            ('admin3', 'admin3'),
            ('dhakkan', 'dumbo'),
            ('admin4', 'admin4');
        `;

        connection.query(initSQL, (error) => {
            if (error) {
                console.log('Database initialization error:', error.message);
            } else {
                console.log('Database initialized successfully');
            }
            connection.end();
        });

    } catch (error) {
        console.error('Database connection error:', error.message);
    }
}

// Create database connection
function getConnection() {
    return mysql.createConnection(dbConfig);
}

// Routes

// Homepage
app.get('/', (req, res) => {
    res.render('index');
});

// UNION-based SQL Injection Lab
app.get('/union', (req, res) => {
    const searchTerm = req.query.name;
    let query = '';
    let results = [];
    let error = '';

    if (searchTerm) {
        query = `SELECT * FROM users WHERE username = '${searchTerm}'`;
        
        const connection = getConnection();
        connection.query(query, (err, rows) => {
            if (err) {
                error = err.message;
            } else {
                results = rows;
            }
            
            res.render('union', {
                searchTerm,
                query,
                results,
                error
            });
            connection.end();
        });
    } else {
        res.render('union', {
            searchTerm: '',
            query: '',
            results: [],
            error: ''
        });
    }
});

// Reflect/Error-based SQL Injection Lab
app.get('/reflect', (req, res) => {
    const searchTerm = req.query.name;
    let query = '';
    let result = '';
    let error = '';

    if (searchTerm) {
        query = `SELECT username FROM users WHERE username = '${searchTerm}'`;
        
        const connection = getConnection();
        connection.query(query, (err, rows) => {
            if (err) {
                error = err.message;
            } else if (rows.length > 0) {
                result = `User found: ${rows[0].username}`;
            } else {
                result = 'No user found';
            }
            
            res.render('reflect', {
                searchTerm,
                query,
                result,
                error
            });
            connection.end();
        });
    } else {
        res.render('reflect', {
            searchTerm: '',
            query: '',
            result: '',
            error: ''
        });
    }
});

// Boolean-based Blind SQL Injection Lab
app.get('/boolean', (req, res) => {
    const searchTerm = req.query.name;
    let query = '';
    let result = '';
    let error = '';

    if (searchTerm) {
        query = `SELECT username FROM users WHERE username = '${searchTerm}'`;
        
        const connection = getConnection();
        connection.query(query, (err, rows) => {
            if (err) {
                result = 'User not exists';
            } else if (rows.length > 0) {
                result = 'User exists';
            } else {
                result = 'User not exists';
            }
            
            res.render('boolean', {
                searchTerm,
                query,
                result,
                error: ''
            });
            connection.end();
        });
    } else {
        res.render('boolean', {
            searchTerm: '',
            query: '',
            result: '',
            error: ''
        });
    }
});

// Time-based Blind SQL Injection Lab
app.get('/time', (req, res) => {
    const searchTerm = req.query.name;
    let query = '';
    let result = '';
    let error = '';

    if (searchTerm) {

        query = `SELECT * FROM users WHERE username = '${searchTerm}'`;
        // const sleepQuery = `SELECT * FROM users WHERE username = '${searchTerm}' AND SLEEP(2)`;
        
        // const startTime = Date.now();
        const connection = getConnection();
        
        connection.query(query, (err, rows) => {
            // const executionTime = Date.now() - startTime;
            
            try {
                if (err) {
                    error = err.message;
                } else {
                    if (rows.length > 0) {
                        result = `Query executed`;
                    } else {
                        result = `Query executed`;
                    }
                }
            } catch (e) {
                result = `Query executed`;
            }

            error = '';
            result = `Query executed`;
            
            res.render('time', {
                searchTerm,
                query,
                result,
                error
            });
            connection.end();
        });
    } else {
        res.render('time', {
            searchTerm: '',
            query: '',
            result: '',
            error: ''
        });
    }
});

// Start server
app.listen(PORT, () => {
    console.log(`SQLi Labs server running on http://localhost:${PORT}`);
    initializeDatabase();
});
