USE G4TF_items;
INSERT INTO `item` (`item_id`, `category`, `item_name`, `item_qty`, `item_desc`, `item_price`, `current_count`, `shipping_count`, `status`, `expiry`) VALUES
('0lc2Cgj5uroiFDq', 'ring', 'Corona 925 Silver Cocktail Ring', 50, 'The simple and classic design of ring embedded with the luminous zircon. This ring oozes the sophisticated style along your finger.', 116, 0, 6, 'pending', '2021-04-18 12:30:13'),
('18jTLCgAibIuVeS', 'ear ring', 'Frankie earrings', 200, 'Wide hoop earrings. An extra thick layer of 14k gold plated with brass base. Steel posts. Approximately 11mm hoops.', 56, 19, 25, 'pending', '2021-04-20 12:30:13'),
('27Hamu4hrLw0qPd', 'ear ring', 'Biar Bridal Hoops', 23, 'The ‘Briar’ bridal hoop earrings are a statement bridal earring made with delicate handcrafted clay flowers and sparkling swarovski crystals. Entirely', 89, 0, 13, 'pending', '2021-04-14 00:00:00'),
('A7mf5FqlCAms3ZW', 'necklace', 'Silver small round medallion necklace', 40, 'Our solid sterling silver small round St Christopher medallion necklace is the perfect gift for a loved one. Excellent for everyday wear, this St Chri', 50.9, 0, 30, 'pending', '2021-04-10 12:30:13'),
('favTYxRMfsbLokG', 'necklace', 'Gold single pearl necklace', 40, 'This elegant necklace is perfect for a bride on her wedding day and subtle enough to be dressed down for a more every day look.', 60, 0, 30, 'pending', '2021-04-18 12:30:13'),
('ftaXI7ybGHm1lfu', 'bracelet', 'Eclipse Cuff', 40, 'The longitudinal and cross sections of the metal remain same color of the original bangle, which enable the color that never fade.', 88, 0, 20, 'pending', '2021-04-18 12:30:13'),
('hnZlIRkRjuT4Gy9', 'ear ring', 'Gambade Clou de Selle earrings', 30, 'Clasp rose gold chain ear ring with 4 diamonds.', 123.9, 0, 50, 'pending', '2021-04-20 12:30:13'),
('jqJ6oK3PLMT8HKv', 'ear ring', 'Anouk earrings', 200, 'Petite hoop charm earrings. Cubic zirconia, an extra thick layer of 14k gold plated with brass base. Approximately 15mm hoop.', 46, 19, 25, 'pending', '2021-04-20 12:30:13'),
('kc5mX0fOK2BXnls', 'ring', 'Contorto 925 Silver Ring', 140, 'The simple and classic design of ring embedded with the luminous zircon. This ring oozes the sophisticated style along your finger.', 133, 0, 20, 'pending', '2021-04-18 12:30:13'),
('NvKwnrAQx9kmrbA', 'ear ring', 'Gambade Clou de Selle earrings', 30, 'Clasp rose gold chain ear ring with 4 diamonds.', 123.9, 0, 50, 'shipping', '2021-04-20 12:30:13'),
('oriEhzOHm9TarSF', 'necklace', 'Le Infinità Open Heart 925 Silver Necklace', 50, 'The heart-shaped pendant with sparkling zircon sways with your movement. This design exudes natural elegance.', 70, 0, 6, 'pending', '2021-04-18 12:30:13'),
('v9OETwCSLkm5g8M', 'ear ring', 'Dani earrings', 233, 'Butterfly wing pair of earrings. Gold plated with brass base and surgical steel posts or sterling silver.', 37, 19, 50, 'pending', '2021-04-20 12:30:13'),
('wUK2TBomHIccsct', 'necklace', 'Silver personalised bar necklace', 90, 'This stunning, vertically engraved bar necklace in solid sterling silver, is hand crafted in London and can be laser engraved to add a special date, n', 33.9, 0, 30, 'pending', '2021-04-19 12:30:13'),
('YKryVjV9rhYlLqW', 'ear ring', 'Finesse earrings', 200, 'Earrings in rose gold set with diamonds. An Hermès icon, the signature toggle clasp becomes a motif. A style both graphic and pure.', 36, 19, 25, 'archived', '2021-04-20 12:30:13');
COMMIT;

INSERT INTO `item_image` (`item_id`, `image_url`) VALUES
('0lc2Cgj5uroiFDq', 'https://www.crudo-leather.com/site/assets/files/2966893/zrg01_wg_model.746x0.webp'),
('18jTLCgAibIuVeS', 'https://cdn.shopify.com/s/files/1/1850/1069/products/062d8f3b-0ec8-4290-a0c8-c8b39d9870d0.jpg?v=1600711782'),
('18jTLCgAibIuVeS', 'https://cdn.shopify.com/s/files/1/1850/1069/products/45e99e77-dcc0-436b-92fa-b6bdbf17bfa3.jpg?v=1600711782'),
('18jTLCgAibIuVeS', 'https://cdn.shopify.com/s/files/1/1850/1069/products/Frankie.jpg?v=1600711782'),
('27Hamu4hrLw0qPd', 'https://www.pswithlove.co.uk/wp-content/uploads/2019/11/Briar-bridal-hoop-earrings-scaled.jpg'),
('2RnTjCY2fL8ouyD', 'https://assets.hermes.com/is/image/hermesproduct/gambade-clou-de-selle-earrings--216532B%2000-worn-2-0-0-1440-1440_b.jpg'),
('A7mf5FqlCAms3ZW', 'https://cdn.shopify.com/s/files/1/0278/4857/2989/products/SilverSmallStChristopherNecklace-Model_600x.jpg?v=1603379563'),
('favTYxRMfsbLokG', 'https://cdn.shopify.com/s/files/1/0278/4857/2989/products/Singlepearlnecklace_600x.jpg?v=1603462068'),
('ftaXI7ybGHm1lfu', 'https://www.crudo-leather.com/site/assets/files/846494/190124_style_2019_white_day_10.746x0.webp'),
('hnZlIRkRjuT4Gy9', 'https://assets.hermes.com/is/image/hermesproduct/gambade-clou-de-selle-earrings--216532B%2000-worn-2-0-0-1440-1440_b.jpg'),
('jqJ6oK3PLMT8HKv', 'https://cdn.shopify.com/s/files/1/1850/1069/products/Anouk.jpeg?v=1565323883'),
('jqJ6oK3PLMT8HKv', 'https://cdn.shopify.com/s/files/1/1850/1069/products/P7120128.jpg?v=1565323883'),
('jqJ6oK3PLMT8HKv', 'https://cdn.shopify.com/s/files/1/1850/1069/products/P7120133_e5e77e25-be0f-469d-9ea2-8724aaa54c88.jpg?v=1565323883'),
('kc5mX0fOK2BXnls', 'https://www.crudo-leather.com/site/assets/files/3013412/zrg02_wg_model.746x0.webp'),
('NvKwnrAQx9kmrbA', 'https://assets.hermes.com/is/image/hermesproduct/gambade-clou-de-selle-earrings--216532B%2000-front-3-300-0-1440-1440_b.jpg'),
('NvKwnrAQx9kmrbA', 'https://assets.hermes.com/is/image/hermesproduct/gambade-clou-de-selle-earrings--216532B%2000-worn-2-0-0-1440-1440_b.jpg'),
('oriEhzOHm9TarSF', 'https://www.crudo-leather.com/site/assets/files/2962549/znk04_rg_model.746x0.webp'),
('s9yy80IH7ZMoF6o', 'https://cdn.shopify.com/s/files/1/1850/1069/products/062d8f3b-0ec8-4290-a0c8-c8b39d9870d0.jpg?v=1600711782'),
('s9yy80IH7ZMoF6o', 'https://cdn.shopify.com/s/files/1/1850/1069/products/45e99e77-dcc0-436b-92fa-b6bdbf17bfa3.jpg?v=1600711782'),
('s9yy80IH7ZMoF6o', 'https://cdn.shopify.com/s/files/1/1850/1069/products/Frankie.jpg?v=1600711782'),
('v9OETwCSLkm5g8M', 'https://cdn.shopify.com/s/files/1/1850/1069/products/7d9c13e6-24fc-40f8-9f8b-b989169de55c.jpg?v=1609879394'),
('v9OETwCSLkm5g8M', 'https://cdn.shopify.com/s/files/1/1850/1069/products/Dani.jpg?v=1609879394'),
('v9OETwCSLkm5g8M', 'https://cdn.shopify.com/s/files/1/1850/1069/products/efa7ad86-5dd0-45dc-b434-9d78e0972356_af2b4ab4-e396-475a-aa77-534514188f3f.jpg?v=1609879394'),
('v9OETwCSLkm5g8M', 'https://cdn.shopify.com/s/files/1/1850/1069/products/P6290075.jpg?v=1606324605'),
('wUK2TBomHIccsct', 'https://cdn.shopify.com/s/files/1/0278/4857/2989/products/THIN_BAR_NECKLACE_-_OSCAR_0100_5eeee590-76cf-4341-8569-5dad62048461_600x.jpg?v=1592997544');
COMMIT;

USE G4TF_users;
INSERT INTO `user_detail` (`user_type`, `user_id`, `user_password`, `fullname`, `email`, `phone_number`) VALUES
('admin', 'OKIIiZ6VzzqwRMG', '$5$rounds=535000$vGDz5OV7a2Kxsxla$JKnaANYXVz6zQxsxH8gavsd5cAwbXNIsEoazO.O/0K.', 'Admin', 'admin@mail.com', '91234567');
