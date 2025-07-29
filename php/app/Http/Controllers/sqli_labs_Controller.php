<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Support\Facades\DB;
use App\Models\sqli_labs;

class sqli_labs_Controller extends Controller
{
    public function index()
    {
        return view('sqli.index');
    }

    // Lab 1: UNION-based SQL Injection
    public function unionLab(Request $request)
    {
        $name = $request->query('name');
        
        if (!$name) {
            return view('sqli.union', [
                'users' => [],
                'query' => null,
                'error' => null,
                'searchTerm' => null
            ]);
        }

        $query = "SELECT id, username, password FROM sqli_users WHERE username = '$name'";
        
        try {
            $users = DB::select($query);
            
            return view('sqli.union', [
                'users' => $users,
                'query' => $query,
                'error' => null,
                'searchTerm' => $name
            ]);
        } catch (\Exception $e) {
            return view('sqli.union', [
                'users' => [],
                'query' => $query,
                'error' => $e->getMessage(),
                'searchTerm' => $name
            ]);
        }
    }

    // Lab 2: Error/Reflect-based SQL Injection
    public function reflectLab(Request $request)
    {
        $name = $request->query('name');
        
        if (!$name) {
            return view('sqli.reflect', [
                'result' => null,
                'query' => null,
                'error' => null,
                'searchTerm' => null
            ]);
        }

        $query = "SELECT username FROM sqli_users WHERE username = '$name' LIMIT 1";
        
        try {
            $result = DB::select($query);
            $message = $result ? "User '{$result[0]->username}' found!" : "User '$name' not found.";
            
            return view('sqli.reflect', [
                'result' => $message,
                'query' => $query,
                'error' => null,
                'searchTerm' => $name
            ]);
        } catch (\Exception $e) {
            return view('sqli.reflect', [
                'result' => null,
                'query' => $query,
                'error' => $e->getMessage(),
                'searchTerm' => $name
            ]);
        }
    }

    // Lab 3: Boolean-based Blind SQL Injection
    public function booleanLab(Request $request)
    {
        $name = $request->query('name');
        
        if (!$name) {
            return view('sqli.boolean', [
                'exists' => null,
                'query' => null,
                'error' => null,
                'searchTerm' => null
            ]);
        }

        $query = "SELECT COUNT(*) as count FROM sqli_users WHERE username = '$name'";
        
        try {
            $result = DB::select($query);
            $exists = $result[0]->count > 0;
            
            return view('sqli.boolean', [
                'exists' => $exists,
                'query' => $query,
                'error' => null,
                'searchTerm' => $name
            ]);
        } catch (\Exception $e) {
            return view('sqli.boolean', [
                'exists' => null,
                'query' => $query,
                'error' => $e->getMessage(),
                'searchTerm' => $name
            ]);
        }
    }

    // Lab 4: Time-based Blind SQL Injection
    public function timeLab(Request $request)
    {
        $name = $request->query('name');
        
        if (!$name) {
            return view('sqli.time', [
                'result' => null,
                'query' => null,
                'error' => null,
                'searchTerm' => null,
                'executionTime' => null
            ]);
        }

        $query = "SELECT username FROM sqli_users WHERE username = '$name'";
        
        $startTime = microtime(true);
        
        try {
            $result = DB::select($query);
        } catch (\Exception $e) {
        }
        
        $endTime = microtime(true);
        $executionTime = round(($endTime - $startTime) * 1000, 2); 
        
        return view('sqli.time', [
            'result' => 'Query executed',
            'query' => $query,
            'error' => null,
            'searchTerm' => $name,
            'executionTime' => $executionTime
        ]);
    }
}
