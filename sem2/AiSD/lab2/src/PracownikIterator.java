import java.util.Iterator;
import java.util.NoSuchElementException;

public class PracownikIterator implements Iterator<Pracownik> {
    private Pracownik[] pracownicy;
    private int position;
    private int size;

    public PracownikIterator(Pracownik[] pracownicy, int size) {
        this.pracownicy = pracownicy;
        this.size = size;
        this.position = 0;
    }

    @Override
    public boolean hasNext() {
        return position < size;
    }

    @Override
    public Pracownik next() throws NoSuchElementException {
        if (!hasNext()) {
            throw new NoSuchElementException();
        }
        return pracownicy[position++];
    }

    public void remove() throws UnsupportedOperationException {
        throw new UnsupportedOperationException();
    }
}
