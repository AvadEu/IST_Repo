package GUI;

import javax.swing.*;
import javax.swing.border.EmptyBorder;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.util.ArrayList;
import java.util.Map;

import static java.util.Map.entry;

public class Śniadanie {

    final private static JTextField orderArea = new JTextField();
    final private static JTextField priceArea = new JTextField();

    final private static Map<String, Double> menu = Map.ofEntries(
            entry("Jajecznica", 16.50),
            entry("Owsianka", 15.25),
            entry("Tosty", 12.00),
            entry("Espresso", 10.00),
            entry("Americano", 8.50)
    );

    final private static ArrayList<String> orderContent= new ArrayList<String>();
    private static double orderPrice = 0;

    public static void main(String[] args) {
        Śniadanie s = new Śniadanie();
        s.guiInit();
    }

    public void guiInit() {

        JFrame frame = new JFrame("Śniadanie");
        GridLayout frame_layout = new GridLayout(1,2);

        JPanel panel1 = new JPanel();
        JPanel panel2 = new JPanel();
        panel1.setLayout(new BoxLayout(panel1, BoxLayout.Y_AXIS));
        panel2.setLayout(new BoxLayout(panel2, BoxLayout.Y_AXIS));

        EmptyBorder decorationBorder = new EmptyBorder(10, 15, 5, 15);

        panel1.setBorder(decorationBorder);
        panel2.setBorder(decorationBorder);

        JCheckBox ch1 = new JCheckBox("Tosty - 12 zł");
        ch1.addActionListener(new CheckBoxReaction());

        JCheckBox[] options = new JCheckBox[menu.size()];

        panel1.add(new JLabel("Menu:"));

        for (int i = 0; i < menu.size(); i++) {
            String menuKey = menu.keySet().toArray()[i].toString();
            options[i] = new JCheckBox(String.format("%s - %.2f zł", menuKey, menu.get(menuKey)));
            options[i].addActionListener(new CheckBoxReaction());
            panel1.add(options[i]);
        }

        JButton orderButton = new JButton("Akceptuj");
        orderButton.addActionListener(new ButtonReaction());
        panel1.add(orderButton);

        orderArea.setEditable(false);
        orderArea.setAlignmentY(Component.CENTER_ALIGNMENT);

        priceArea.setEditable(false);
        orderArea.setAlignmentY(Component.CENTER_ALIGNMENT);

        panel2.add(new JLabel("Moje śniadanie:"));
        panel2.add(orderArea);
        panel2.add(new JLabel("Kwota do zapłaty:"));
        panel2.add(priceArea);

        frame.setLayout(frame_layout);
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.getContentPane().add(panel1);
        frame.getContentPane().add(panel2);
        frame.setSize(500, 225);
        frame.setVisible(true);
    }

    class CheckBoxReaction implements ActionListener {
        public void actionPerformed(ActionEvent e) {

            JCheckBox activated = (JCheckBox) e.getSource();

            String key = getFirstWord(activated.getText());

            if (activated.isSelected()) {
                orderPrice += menu.get(key);
                orderContent.add(key);
            } else {
                orderPrice -= menu.get(key);
                orderContent.remove(key);
            }
        }
    }

    class ButtonReaction implements ActionListener {
        public void actionPerformed(ActionEvent e) {
            priceArea.setText(String.valueOf(orderPrice));
            orderArea.setText(getOrderContent(orderContent));
        }
    }

    public static String getFirstWord(String s) {
        return s.split(" ")[0];
    }

    public static String getOrderContent(ArrayList<String> orderContent) {
        String content = "";
        for (int i = 0; i < orderContent.size() - 1; i++) {
            content += orderContent.get(i);
            content += ", ";
        }
        content += orderContent.getLast();
        return content;
    }
}
