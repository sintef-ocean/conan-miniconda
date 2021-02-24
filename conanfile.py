from conans import ConanFile, CMake, tools
import os

class MinicondaConan(ConanFile):
    name = "miniconda"
    version = "4.9.2"
    license = ("BSD-Clause-3",)
    author = "SINTEF Ocean"
    url = "https://github.com/sintef-ocean/conan-miniconda"
    description = "Conda is an open-source package management system"
    topics = ("Miniconda", "Conda")
    settings = {"os": ["Windows"], "arch": ["x86_64"]}
    options = {
        "packages": "ANY",
        "channels": "ANY"
    }
    default_options = {
        "packages": "flang,clangdev,perl,libflang", 
        "channels": "conda-forge"
    }
    no_copy_source = True
    short_paths = True
    _pythonversion = 38
    generators = "virtualenv"
    
    @property
    def _packages(self):
        packs = str(self.options.get_safe("packages", default=""))
        if not packs:
            return ""
        return " ".join(packs.split(','))
    
    def _channels(self):
        chans = str(self.options.get_safe("channels", default=""))
        if not chans:
            return []
        return chans.split(',')
    
    @property
    def _platform(self):
        return {"Windows": "Windows",
                "Macos": "MacOSX",
                "Linux": "Linux"}.get(str(self.settings.os))
                
    @property
    def _suffix(self):
        return {"Windows": "exe",
                "Macos": "sh",
                "Linux": "sh"}.get(str(self.settings.os))
    
    @property
    def _installer(self):
        return "Miniconda3-py{}_{}-{}-{}.{}".format(
            self._pythonversion, 
            self.version, 
            self._platform, 
            self.settings.arch,
            self._suffix)
    
    def configure(self):
        if self.settings.os != "Windows":
            raise ConanInvalidConfiguration("Recipe is only implemented for Windows")
        pass
    
    def source(self):
    
        source_url = "https://repo.anaconda.com/miniconda/" + self._installer
        # https://docs.conda.io/en/latest/miniconda_hashes.html
        sha256 = {
            "Windows": "4fa22bba0497babb5b6608cb8843545372a99f5331c8120099ae1d803f627c61",
            "Macos": "a9ea0afba55b5d872e01323d495b649eac8ff4ce2ea098fb4c357b6139fe6478",
            "Linux": "1314b90489f154602fd794accfc90446111514a5a72fe1f71ab83e07de9504a7"}\
            .get(str(self.settings.os))
    
        tools.download(source_url, self._installer, sha256=sha256)

    def build(self):
        
        self.output.info("Running conda installer..")
        install_path = os.path.join(self.build_folder, "miniconda3")
        install_options = " /RegisterPython=0 /S "
        install_options += "/D=" + install_path
        self.run(os.path.join(self.source_folder,
                              self._installer) + install_options)

        env_info = { "PATH" : [os.path.join(install_path, "condabin")] }

        with tools.environment_append(env_info):
            # self.output.info("Conda config --show:")
            # self.run("conda config --show")
            if len(self._channels()):
                self.output.info("Adding channels")
                for channel in self._channels():
                    self.run("conda config --add channels {}".format(channel))
            if self._packages:
                self.output.info("Installing packages") 
                self.run("conda install -y {}".format(self._packages))
        
    def package(self):
        self.copy(pattern="*", src="miniconda3", keep_path=True, symlinks=True)
        
    def package_info(self):
        self.output.info("Exporting CONDA environment")
        self.env_info.PATH.append(
            os.path.join(self.package_folder, "condabin"))
        self.output.warn(
            "This recipe may conflict with your existing conda installation, "
            "see `conda config --show` with (conan) virtualenv active")

    def package_id(self):
        del self.info.options.packages
        del self.info.options.channels