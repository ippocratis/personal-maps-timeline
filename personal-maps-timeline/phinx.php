<?php

require 'config.php';

return [
    'paths' => [
        'migrations' => '%%PHINX_CONFIG_DIR%%/db/migrations',
        'seeds' => '%%PHINX_CONFIG_DIR%%/db/seeds'
    ],
    'environments' => [
        'default_migration_table' => 'phinxlog',
        'default_environment' => 'development',
        'production' => [
            'adapter' => 'mysql',
            'host' => 'db',  // Corrected to use DB_HOST
            'name' => 'personal_location_history',
            'user' => 'root',
            'pass' => 'example',
            'port' => '3306',
            'charset' => 'utf8mb4',
            'collation' => 'utf8mb4_unicode_ci',
        ],
        'development' => [
            'adapter' => 'mysql',
            'host' => 'db',  // Corrected to use DB_HOST
            'name' => 'personal_location_history', // Fixed quote
            'user' => 'root',
            'pass' => 'example', // Fixed quote
            'port' => '3306',
            'charset' => 'utf8mb4',
            'collation' => 'utf8mb4_unicode_ci',
        ],
        'testing' => [
            'adapter' => 'mysql',
            'host' => 'db',  // Corrected to use DB_HOST
            'name' => 'personal_location_history',
            'user' => 'root',
            'pass' => 'example',
            'port' => '3306',
            'charset' => 'utf8mb4',
            'collation' => 'utf8mb4_unicode_ci',
        ]
    ],
    'version_order' => 'creation'
];
