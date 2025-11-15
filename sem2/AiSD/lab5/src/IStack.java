public interface IStack<E> {
    public void push(E e);
    public E pop();
    public int size();
    public boolean isEmpty();
}
