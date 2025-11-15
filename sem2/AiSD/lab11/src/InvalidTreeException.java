public class InvalidTreeException extends Exception{

    @Override
    public void printStackTrace() {
        System.out.println("Nieprawidłowe drzewo kodu!");
    }
}