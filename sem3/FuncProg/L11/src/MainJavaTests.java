
// Proste pola prywatne
class Cat {
    private String name;
    private int age;

    public Cat(String name, int age) {
        this.name = name;
        this.age = age;
    }
}

// Pola statyczne i const
class MathConstant {
    public final double PI = 3.14159;
    private static String TYPE = "Math";
    double value;

    public MathConstant(double value) {
        this.value = value;
    }
}

class Engine {
    @Override
    public String toString() { return "V8 Turbo"; }
}

class Car {
    private String model;
    private Engine engine;

    public Car(String model) {
        this.model = model;
        this.engine = new Engine();
    }
}

class Animal {
    int id = 1;
}
class Dog extends Animal {
    String breed = "Labrador";
}

public class MainJavaTests {
    public static void main(String[] args) {
        Debug debugger = new Debug();

        System.out.println("Test 1: Cat (pola prywatne)");
        Cat myCat = new Cat("Filemon", 2);
        debugger.fields(myCat);

        System.out.println("Test 2: MathConstant (pola finalne i statyczne)");
        MathConstant math = new MathConstant(10.5);
        debugger.fields(math);

        System.out.println("Test 3: Car (pole obiektowe)");
        Car myCar = new Car("Mustang");
        debugger.fields(myCar);

        System.out.println("Test 4: Dog (dziedziczenie - sprawdzamy czy widać pola rodzica)");
        Dog myDog = new Dog();
        debugger.fields(myDog);

        System.out.println("Test 5: Null");
        debugger.fields(null);
    }
}