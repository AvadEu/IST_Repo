public interface IStack<T> {
    public boolean isEmpty();

    public boolean isFull();

    public void push(T item);

    public T pop();

    public int size();
}
