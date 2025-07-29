<?php

use App\Http\Controllers\sqli_labs_Controller;
use Illuminate\Support\Facades\Route;

// SQLi Labs routes - moved to root
Route::get('/', [sqli_labs_Controller::class, 'index'])->name('sqli.index');

// Lab 1: UNION-based SQL Injection
Route::get('/union', [sqli_labs_Controller::class, 'unionLab'])->name('sqli.union');

// Lab 2: Error/Reflect-based SQL Injection
Route::get('/reflect', [sqli_labs_Controller::class, 'reflectLab'])->name('sqli.reflect');

// Lab 3: Boolean-based Blind SQL Injection
Route::get('/boolean', [sqli_labs_Controller::class, 'booleanLab'])->name('sqli.boolean');

// Lab 4: Time-based Blind SQL Injection
Route::get('/time', [sqli_labs_Controller::class, 'timeLab'])->name('sqli.time');
