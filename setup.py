from distutils.core import setup
from distutils import util
from pathlib import Path

if __name__ == "__main__":
    # package paths
    tcheasyPath = util.convert_path("tcheasy")

    # get version file
    versionPath = Path().cwd() / "tcheasy/version.py"

    main_ns = {}

    with open(str(versionPath)) as ver_file:
        exec(ver_file.read(), main_ns)

    # running setup
    setup(
        name="tcheasy",
        version=main_ns['__version__'],
        description="A python decorator which checks types & restrictions for user inputs",
        author="Daniel Kiermeier",
        author_email="d.kiermeier@layers-of-life.com",
        url="https://github.com/No9005/tcheasy",
        download_url="",
        license="MIT",
        package_dir={
            "tcheasy":tcheasyPath
        },
        packages=["tcheasy"],
        python_reqires='>3.8.5'
    )