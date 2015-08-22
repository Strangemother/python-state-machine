import cli.app
import demos


@cli.app.CommandLineApp
def main(app):
    print 'Run machine'
    demos.run()


@cli.app.CommandLineApp
def ls(app):
    pass

ls.add_param("-l", "--long", help="list in long format", default=False, action="store_true")

def main():
    print 'Run machine'
    demos.run()

if __name__ == '__main__':
    import pdb; pdb.set_trace()
    main()
