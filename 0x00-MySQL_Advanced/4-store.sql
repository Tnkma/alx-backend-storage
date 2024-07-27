-- creates a trigger that decreses the quantity when a new insert is made

DELIMITER //

CREATE TRIGGER after_order_insert
AFTER INSERT ON orders
FOR EACH ROW
BEGIN
    -- Decrease the quantity of the item in the items table
    UPDATE items
    SET quantity = quantity - NEW.number
    WHERE name = NEW.item_name;
END //

DELIMITER ;
