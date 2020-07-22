
CREATE TABLE if not exists `users` ( `id` varchar ( 200 ), `password` varchar ( 255 ) NOT NULL, `user_name` varchar ( 200 ) NOT NULL UNIQUE, `role_id` NUMERIC NOT NULL, `created_at` datetime NOT NULL, `updated_at` datetime NOT NULL, `name` varchar ( 200 ), `is_deleted` bool NOT NULL, PRIMARY KEY(`id`) );

CREATE TABLE if not exists `projects` ( `id` varchar ( 200 ), `name` varchar ( 200 ) NOT NULL, `total_labour_required` int NOT NULL, `estimated_cost` int NOT NULL, `area_of_project` int NOT NULL, `estimated_start_date` datetime NOT NULL, `estimated_end_date` datetime NOT NULL, `gpm_id` varchar ( 200 ) NOT NULL, `created_by` varchar ( 200 ) NOT NULL, `project_type` varchar ( 200 ) NOT NULL, `is_deleted` bool NOT NULL, PRIMARY KEY(`id`), FOREIGN KEY(`gpm_id`) REFERENCES `users`(`id`), FOREIGN KEY(`created_by`) REFERENCES `users`(`id`) );

CREATE TABLE if not exists `personal_details` ( `user_id` varchar ( 200 ) NOT NULL UNIQUE, `state` varchar ( 150 ) NOT NULL, `district` varchar ( 150 ) NOT NULL, `pincode` int NOT NULL, `age` int NOT NULL, `gender` varchar ( 50 ) NOT NULL, `created_by` varchar ( 200 ) NOT NULL, FOREIGN KEY(`created_by`) REFERENCES `users`(`id`), FOREIGN KEY(`user_id`) REFERENCES `users`(`id`) );

CREATE TABLE if not exists `project_members` ( `project_id` varchar ( 200 ) NOT NULL, `member_id` varchar ( 200 ) NOT NULL unique, `assigned_date` datetime NOT NULL, FOREIGN KEY(`project_id`) REFERENCES `projects`(`id`), FOREIGN KEY(`member_id`) REFERENCES `user`(`id`));

CREATE TABLE if not exists  `completed_project_members` ( `project_id` varchar ( 200 ) NOT NULL, `member_id` varchar ( 200 ) NOT NULL , `assigned_date` datetime NOT NULL, `completion_date` datetime NOT NULL, `wage` int NOT NULL, FOREIGN KEY(`project_id`) REFERENCES `projects`(`id`), FOREIGN KEY(`member_id`) REFERENCES `user`(`id`));

CREATE TABLE if not exists `requests` ( `type` int NOT NULL, `raised_by` varchar ( 200 ) NOT NULL, `request_msg` varchar NOT NULL, `is_accepted` bool, `issued_on` datetime NOT NULL, `resolved_on` datetime, `raised_for` varchar ( 200 ) NOT NULL, `id` varchar ( 200 ), FOREIGN KEY(`raised_by`) REFERENCES `users`(`id`), PRIMARY KEY(`id`), FOREIGN KEY(`raised_for`) REFERENCES `users`(`id`) );

insert into `users`
select  '683e42e4-fa24-4b98-9ff8-bbfc0400ffe9', 'c2MAArAollkaUkCBYjud9KygSwGJnyWboEzjWgZ3E/FjBwiSGn+ktUofBD2QIK77xdkSAgxLf/M2i5K2Rr/CQec0ASiwZQoZ', 'SAMPLE_BDO',1,'2020-01-01','2020-01-01', 'SAMPLE_BDO', 'False'
Where not exists(select * from `users` where id='683e42e4-fa24-4b98-9ff8-bbfc0400ffe9')