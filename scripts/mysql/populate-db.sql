USE `community`;

INSERT INTO `user` (`id`, `username`, `name`) VALUES (1, 'jdoe', 'Jane Doe');
INSERT INTO `user` (`id`, `username`, `name`) VALUES (2, 'jqpublic', 'John Q Public');

INSERT INTO `question` (`id`, `asker_id`, `title`) VALUES (1, 1, 'How do you keep the weight off?');

INSERT INTO `response` (`id`, `responder_id`, `question_id`, `text`) VALUES (1, 2, 1, 'Diet and exercise');

INSERT INTO `questionbookmark` (`id`, `user_id`, `question_id`) VALUES (1, 1, 1);

INSERT INTO `responsebookmark` (`id`, `user_id`, `response_id`) VALUES (1, 1, 1);
