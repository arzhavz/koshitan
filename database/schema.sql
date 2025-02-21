CREATE TABLE IF NOT EXISTS `warns` (
  `id` int(11) NOT NULL,
  `user_id` varchar(20) NOT NULL,
  `server_id` varchar(20) NOT NULL,
  `moderator_id` varchar(20) NOT NULL,
  `reason` varchar(255) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS `users` (
  `id` INTEGER PRIMARY KEY AUTOINCREMENT,
  `user_id` INTEGER UNIQUE NOT NULL,
  `level` INTEGER NOT NULL,
  `exp` INTEGER NOT NULL,
  `money` INTEGER NOT NULL,
  `crate` JSON,
  `item` JSON,
  `energy` JSON,
  `orb` JSON,
  `soul` JSON,
  `character` JSON,
  `character_showdown` JSON,
  `character_equipment` JSON,
  `battle_session` JSON                   
);