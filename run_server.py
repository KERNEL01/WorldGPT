from worldgpt.shared.util.subsystem import Subsystem


def bootstrap_subsystems():
    """ Instantiates and Bootstraps all subsystems."""
    for subcls in Subsystem.__subclasses__():
        subcls().bootstrap()


def shutdown_subsystems():
    """ Shuts down all subsystems."""
    for subcls in Subsystem.__subclasses__():
        subcls().queue.put(None)


def main():
    #init_logging()
    bootstrap_subsystems()
    try:
        while True:
            pass # todo APISubsystem.run_in_main_thread()
    except KeyboardInterrupt:
        shutdown_subsystems()


if __name__ == '__main__':
    main()
