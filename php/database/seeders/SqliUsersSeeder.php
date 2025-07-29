<?php

namespace Database\Seeders;

use Illuminate\Database\Seeder;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Hash;

class SqliUsersSeeder extends Seeder
{
    public function run(): void
    {
        DB::table('sqli_users')->insert([
            [
                'id' => 1,
                'username' => 'Dumb',
                'email' => 'admin@example.com',
                'password' => 'Dumb',
                'created_at' => now(),
                'updated_at' => now(),
            ],
            [
                'id' => 2,
                'username' => 'Angelina',
                'email' => 'john@example.com',
                'password' => 'I-kill-you',
                'created_at' => now(),
                'updated_at' => now(),
            ],
            [
                'id' => 3,
                'username' => 'Dummy',
                'email' => 'jane@example.com',
                'password' => 'p@ssword',
                'created_at' => now(),
                'updated_at' => now(),
            ],
            [
                'id' => 4,
                'username' => 'secure',
                'email' => 'test@example.com',
                'password' => 'crappy',
                'created_at' => now(),
                'updated_at' => now(),
            ],
            [
                'id' => 5,
                'username' => 'stupid',
                'email' => 'stupid@example.com',
                'password' => 'stupidity',
                'created_at' => now(),
                'updated_at' => now(),
            ],
            [
                'id' => 6,
                'username' => 'superman',
                'email' => 'superman@example.com',
                'password' => 'genious',
                'created_at' => now(),
                'updated_at' => now(),
            ],
            [
                'id' => 7,
                'username' => 'batman',
                'email' => 'batman@example.com',
                'password' => 'mob!le',
                'created_at' => now(),
                'updated_at' => now(),
            ],
            [
                'id' => 8,
                'username' => 'admin',
                'email' => 'admin2@example.com',
                'password' => 'admin',
                'created_at' => now(),
                'updated_at' => now(),
            ],
            [
                'id' => 9,
                'username' => 'admin1',
                'email' => 'admin1@example.com',
                'password' => 'admin1',
                'created_at' => now(),
                'updated_at' => now(),
            ],
            [
                'id' => 10,
                'username' => 'admin2',
                'email' => 'admin2test@example.com',
                'password' => 'admin2',
                'created_at' => now(),
                'updated_at' => now(),
            ],
            [
                'id' => 11,
                'username' => 'admin3',
                'email' => 'admin3@example.com',
                'password' => 'admin3',
                'created_at' => now(),
                'updated_at' => now(),
            ],

        ]);
    }
}