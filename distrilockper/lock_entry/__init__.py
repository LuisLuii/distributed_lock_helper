"""

public class RedissonLockEntry implements PubSubEntry<RedissonLockEntry> {

    private int counter;

    private final Semaphore latch;
    private final RPromise<RedissonLockEntry> promise;
    private final ConcurrentLinkedQueue<Runnable> listeners = new ConcurrentLinkedQueue<Runnable>();

    public RedissonLockEntry(RPromise<RedissonLockEntry> promise) {
        super();
        this.latch = new Semaphore(0);
        this.promise = promise;
    }

    public void acquire() {
        counter++;
    }

    public int release() {
        return --counter;
    }

    public RPromise<RedissonLockEntry> getPromise() {
        return promise;
    }

    public void addListener(Runnable listener) {
        listeners.add(listener);
    }

    public boolean removeListener(Runnable listener) {
        return listeners.remove(listener);
    }

    public ConcurrentLinkedQueue<Runnable> getListeners() {
        return listeners;
    }

    public Semaphore getLatch() {
        return latch;
    }

}


"""