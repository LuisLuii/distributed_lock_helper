from lock_helper.util.linked_dictionary import LinkedDict

class ExpirationFactory(object):
    def __init__(self):
        self.thread_ids = LinkedDict()
        self.timeout = None

    def add_thread_id(self,thread_id):
        """
        Integer counter = threadIds.get(threadId);
        if (counter == null) {
            counter = 1;
        } else {
            counter++;
        }
        threadIds.put(threadId, counter);
        :param thread_id:
        :return:
        """
        counter = self.thread_ids.get(thread_id)
        if not counter:
            counter = 1
        else:
            counter += 1
        self.thread_ids.put({thread_id:counter})

    def has_no_threds(self):
        return self.thread_ids.empty()

    def get_first_thread_id(self):
        if self.thread_ids.empty:
            return None
        return self.thread_ids.get_first

    def remove_thread_id(self,thread_id):
        """
         if (counter == null) {
             return;
         }
         counter--;
         if (counter == 0) {
             threadIds.remove(threadId);
         } else {
             threadIds.put(threadId, counter);
         }
        :param thread_id:
        :return:
        """
        counter:int = self.thread_ids.get(thread_id)
        if counter == None:
            return
        counter -= 1
        if counter == 0:
            self.thread_ids.remove_thread_id(thread_id)
        else:
            self.thread_ids.put({thread_id:counter})

    def set_timeout(self, timeout):
        self.timeout = timeout

    @property
    def get_timeout(self):
        return self.timeout

if __name__ == '__main__':
    a = ExpirationFactory()
    a.add_thread_id('adddd')
    a.add_thread_id('adddd')
    a.add_thread_id('adddd')