from pydispatch import Dispatcher

class EventManager(Dispatcher):
    # Events are defined in classes and subclasses with the '_events_' attribute
    _events_ = [
        'on_actor_removed', 
        'on_actor_added',
        'on_horizontal_bounds_max_col',
        'on_horizontal_bounds_min_col']
    
    def __init__(self):
        self.events = []

    def enqueue(self, event):
        self.events.append(event)

    def dispatchEvents(self):
        while len(self.events) > 0:
            event = self.events.pop(0)
            self.emit(event.get('name'), data = event.get('data', False))

    # def do_some_stuff(self):
    #     # do stuff that makes new data
    #     data = self.get_some_data()
    #     # Then emit the change with optional positional and keyword arguments
    #     self.emit('new_data', data=data)

# class MyListener(object):
#     def on_new_data(self, *args, **kwargs):
#         data = kwargs.get('data')
#         print('I got data: {}'.format(data))
#     def on_emitter_state(self, *args, **kwargs):
#         print('emitter state changed')

# emitter = MyEmitter()
# listener = MyListener()

# emitter.bind(on_state=listener.on_emitter_state)
# emitter.bind(new_data=listener.on_new_data)

# emitter.do_some_stuff()
# # >>> I got data: ...

# emitter.emit('on_state')
# # >>> emitter state changed