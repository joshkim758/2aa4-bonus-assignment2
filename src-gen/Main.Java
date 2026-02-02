import java.util.*;

public class Main {
    public static void main(String[] args) {

        Address deliveryAddress = new Address();

        Customer customer = new Customer();

        Courier courier = new Courier();

        Menu menu = new Menu();
        MenuItem pizza = new MenuItem();
        MenuItem salad = new MenuItem();

        Order order = new Order();
        
        List<MenuItem> items = new ArrayList<>();
        items.add(pizza);
        items.add(salad);
        
        System.out.println("Order structure established with " + items.size() + " items.");
        
        Delivery delivery = new Delivery();
    }
}