package Order;

import java.util.HashMap;
import java.util.Map;

public class Order {
    private Map<String, Integer> products; // Produkty i ich ilości
    private String shippingMethod;
    private String paymentMethod;

    private Order(OrderBuilder builder) {
        this.products = builder.products;
        this.shippingMethod = builder.shippingMethod;
        this.paymentMethod = builder.paymentMethod;
    }

    public String getOrderDetails() {
        StringBuilder details = new StringBuilder("Produkty:\n");
        for (Map.Entry<String, Integer> entry : products.entrySet()) {
            details.append("- ").append(entry.getKey()).append(": ").append(entry.getValue()).append("\n");
        }
        details.append("Dostawa: ").append(shippingMethod).append("\n");
        details.append("Metoda Płatności: ").append(paymentMethod).append("\n");
        return details.toString();
    }

    public static class OrderBuilder implements Builder {
        public Map<String, Integer> products = new HashMap<>();
        private String shippingMethod;
        private String paymentMethod;

        public OrderBuilder addProduct(String product, int quantity) {
            products.put(product, quantity);
            return this;
        }

        public OrderBuilder setShippingMethod(String shippingMethod) {
            this.shippingMethod = shippingMethod;
            return this;
        }

        public OrderBuilder setPaymentMethod(String paymentMethod) {
            this.paymentMethod = paymentMethod;
            return this;
        }

        @Override
        public Order build() {
            return new Order(this);
        }
    }
}
