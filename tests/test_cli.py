from pathlib import Path

from click.testing import CliRunner

from kvadratnet import knet

def _create_empty_files(files):
    """
    Create empty files from a list of file names
    """
    for filename in files:
        open(filename, 'w').close()


def _glob_files(filespec):
    """
    Return a sorted filelist expanded from 'filespec'
    """
    return sorted(Path('.').glob("*.tif"))

def test_rename():
    """
    Test 'knet rename' command
    """
    runner = CliRunner()
    files = ['pre_1km_6090_600_post.tif', 'pre_1km_6090_601_post.tif']
    with runner.isolated_filesystem():
        _create_empty_files(files)
        args = files
        result = runner.invoke(knet.rename, args)
        print(result.output)
        print(result.exc_info)

        for filename, value in zip(files, _glob_files("*.tif")):
            truth = filename.replace("pre_", "").replace("_post", "")
            assert truth == str(value)

        assert result.exit_code == 0

def test_rename_verbose():
    """
    Test 'knet rename' command
    """
    runner = CliRunner()
    files = ['pre_1km_6090_600_post.tif', 'pre_1km_6090_601_post.tif']
    with runner.isolated_filesystem():
        _create_empty_files(files)
        args = ['--verbose'] + files
        result = runner.invoke(knet.rename, args)
        print(result.output)
        print(result.exc_info)

        for filename, value in zip(files, _glob_files("*.tif")):
            truth = filename.replace("pre_", "").replace("_post", "")
            assert truth == str(value)

        for filename, value in zip(files, result.output.split("\n")):
            renamed = filename.replace("pre_", "").replace("_post", "")
            truth = "Renaming {src} to {dst}".format(src=filename, dst=renamed)
            assert truth == value

        assert result.exit_code == 0


def test_rename_prefix():
    """
    Test 'knet rename --prefix' command
    """
    runner = CliRunner()
    files = ['1km_6090_600.tif', '1km_6090_601.tif']
    with runner.isolated_filesystem():
        _create_empty_files(files)
        prefix = "dtm_"
        args = ["--prefix", prefix] + files
        result = runner.invoke(knet.rename, args)
        print(result.output)
        print(result.exc_info)

        for truth, value in zip(files, _glob_files("*.tif")):
            assert prefix + truth  == str(value)

        assert result.exit_code == 0

def test_rename_postfix():
    """
    Test 'knet rename --postfix' command
    """
    runner = CliRunner()
    files = ['1km_6090_600.tif', '1km_6090_601.tif']
    with runner.isolated_filesystem():
        _create_empty_files(files)
        postfix = "_renamed"
        args = ["--postfix", postfix] + files
        result = runner.invoke(knet.rename, args)
        print(result.output)
        print(result.exc_info)

        for truth, value in zip(files, _glob_files("*.tif")):
            assert truth.replace(".tif", postfix+".tif")  == str(value)

        assert result.exit_code == 0



