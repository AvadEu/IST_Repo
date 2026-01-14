import java.lang.reflect.Field;

public class Debug {

    public void fields(Object obj) {
        if (obj == null) {
            System.out.println("Przekazano obiekt null.");
            return;
        }

        Class<?> clazz = obj.getClass();

        System.out.println("Klasa: " + clazz.getSimpleName());

        Field[] fields = clazz.getDeclaredFields();

        for (Field field : fields) {
            try {
                field.setAccessible(true);

                String name = field.getName();
                String type = field.getType().getSimpleName();
                Object value = field.get(obj);

                System.out.println("Pole: " + name + " => " + type + ", " + value);

            } catch (IllegalAccessException e) {
                System.out.println("Brak dostępu do pola: " + field.getName());
            }
        }
        System.out.println("--------------------");
    }
}