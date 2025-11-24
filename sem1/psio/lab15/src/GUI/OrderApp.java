package GUI;

import Order.Order;

import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.util.ArrayList;
import java.util.List;

public class OrderApp {

    static Order.OrderBuilder orderBuilder = new Order.OrderBuilder();

    public static void run() {
        List<Order> allOrders = new ArrayList<>();

        JFrame frame = new JFrame("Kreator zamówień.");
        frame.setSize(1024, 576);
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.setLayout(new BorderLayout());

        JPanel productPanel = new JPanel();
        productPanel.setBorder(BorderFactory.createTitledBorder("Dodaj produkt"));
        String[] products = {"Laptop", "Telefon", "Drukarka", "Szafa RACK", "Router", "Serwer"};
        JComboBox<String> productComboBox = new JComboBox<>(products);
        JTextField quantityField = new JTextField(5);
        JButton addProductButton = new JButton("Dodaj produkt");
        productPanel.add(new JLabel("Produkt:"));
        productPanel.add(productComboBox);
        productPanel.add(new JLabel("Ilość:"));
        productPanel.add(quantityField);
        productPanel.add(addProductButton);

        // Panel do wyboru metody wysyłki
        JPanel shippingPanel = new JPanel();
        shippingPanel.setBorder(BorderFactory.createTitledBorder("Dostawa:"));
        String[] shippingMethods = {"Standardowa", "Ekspresowa", "Zagraniczna"};
        JComboBox<String> shippingComboBox = new JComboBox<>(shippingMethods);
        shippingPanel.add(shippingComboBox);

        // Panel do wyboru metody płatności
        JPanel paymentPanel = new JPanel();
        paymentPanel.setBorder(BorderFactory.createTitledBorder("Sposób płatności:"));
        String[] paymentMethods = {"Karta Kredytowa", "PayPal", "BLIK"};
        JComboBox<String> paymentComboBox = new JComboBox<>(paymentMethods);
        paymentPanel.add(paymentComboBox);

        JTextArea currentOrderDetails = new JTextArea(10, 30);
        currentOrderDetails.setEditable(false);

        JTextArea allOrdersDetails = new JTextArea(10, 30);
        allOrdersDetails.setEditable(false);

        JButton submitButton = new JButton("Złóż zamówienie");

        class AddProductAction implements ActionListener {
            @Override
            public void actionPerformed(ActionEvent e) {
                String product = (String) productComboBox.getSelectedItem();
                int quantity;

                try {
                    quantity = Integer.parseInt(quantityField.getText());
                    if (quantity <= 0) throw new NumberFormatException();
                } catch (NumberFormatException ex) {
                    JOptionPane.showMessageDialog(frame, "Niepoprawna ilość!", "Error", JOptionPane.ERROR_MESSAGE);
                    return;
                }

                orderBuilder.addProduct(product, quantity);

                currentOrderDetails.setText(orderBuilder.products.toString());
                quantityField.setText("");
            }
        }

        class submitButtonAction implements ActionListener {
            @Override
            public void actionPerformed(ActionEvent e) {
                if (orderBuilder.products.isEmpty()) {
                    JOptionPane.showMessageDialog(frame,
                            "Dodaj produkty przed złożeniem zamówienia!",
                            "Brak produktów!",
                            JOptionPane.WARNING_MESSAGE);
                    return;
                }

                orderBuilder
                        .setShippingMethod((String) shippingComboBox.getSelectedItem())
                        .setPaymentMethod((String) paymentComboBox.getSelectedItem());

                Order order = orderBuilder.build();
                allOrders.add(order);

                StringBuilder allOrdersText = new StringBuilder();
                for (Order o : allOrders) {
                    allOrdersText.append(o.getOrderDetails()).append("\n---\n");
                }
                allOrdersDetails.setText(allOrdersText.toString());

                orderBuilder = new Order.OrderBuilder();
                currentOrderDetails.setText("");
            }
        }

        addProductButton.addActionListener(new AddProductAction());
        submitButton.addActionListener(new submitButtonAction());

        JPanel inputPanel = new JPanel(new GridLayout(3, 1));
        inputPanel.add(productPanel);
        inputPanel.add(shippingPanel);
        inputPanel.add(paymentPanel);

        frame.add(inputPanel, BorderLayout.NORTH);
        frame.add(submitButton, BorderLayout.SOUTH);
        JPanel outputPanel = new JPanel(new GridLayout(1, 2));
        JPanel currentPanel = new JPanel(new BorderLayout());
        JPanel previousPanel = new JPanel(new BorderLayout());

        currentPanel.add(new JLabel("Obecne zamówienie:"), BorderLayout.NORTH);
        currentPanel.add(new JScrollPane(currentOrderDetails), BorderLayout.CENTER);
        previousPanel.add(new JLabel("Poprzednie zamówienia:"), BorderLayout.NORTH);
        previousPanel.add(new JScrollPane(allOrdersDetails), BorderLayout.CENTER);

        outputPanel.add(currentPanel);
        outputPanel.add(previousPanel);

        frame.add(outputPanel, BorderLayout.CENTER);

        frame.setVisible(true);
    }
}
