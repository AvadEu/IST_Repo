public class ListStack<E> implements IStack<E> {
    private L1KPzG<E> list;

    public ListStack() {
        list = new L1KPzG<>();
    }

    @Override
    public void push(E element) {
        list.add(element);
    }

    @Override
    public E pop() {
        return list.removeFirst();
    }

    @Override
    public boolean isEmpty() {
        return list.isEmpty();
    }

    @Override
    public int size() {
        return list.size();
    }
}
