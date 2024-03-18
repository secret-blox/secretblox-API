CREATE TABLE `session` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `client_key` varchar(255) DEFAULT NULL,
  `session_id` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=75 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;insert into `session` (`client_key`, `created_at`, `id`, `session_id`) values ('test', '2024-03-17 21:04:44', 73, 'dGVzdC0xNzEwNzM0Njg0LTRlYjg3NWRjNzM4NWViYjgzMWI2');
insert into `session` (`client_key`, `created_at`, `id`, `session_id`) values ('test', '2024-03-17 21:10:07', 74, 'dGVzdC0xNzEwNzM1MDA3LTM5ZDI4OWVmMGQ2YjNkOTljMjM5');
