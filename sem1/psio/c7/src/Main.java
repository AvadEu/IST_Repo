public class Main {
    public static void main(String[] args) {
        FlyingVechicle airport[] = new FlyingVechicle[3];
//        Plane[] hangar = new Plane[2];

        airport[0] = new Baloon(1000, 1, "czarny");
        airport[1] = new PrivateJet("Gulfstream", 8000, 5000, 1000000, 6);
        airport[2] = new MilitaryJet(12000, "F-22", 8000, "raptor", 10);

        ((Baloon)(airport[0])).addPassenger(new Passenger("Nowak Michał", 78));
        System.out.println(airport[0].toString());

        // Naprawa samolotu
        System.out.println(airport[2].toString());
        Mechanic.repairPlane(((Plane)airport[2]));
        System.out.println(airport[2].toString());

        for (int i  = 0; i < airport.length; i++) {
            if (airport[i] != null) {
                System.out.println(airport[i].toString());
            }
        }
    }

}
