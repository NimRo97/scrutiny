from scrutiny.interfaces import Module


class GPInfo(Module):

    def __init__(self, module_name="GPPro Basic Info"):
        super().__init__(module_name)
        self.iin = None
        self.cin = None
        self.supports = []
        self.versions = []
        self.other = []


class GPList(Module):

    def __init__(self, module_name="GPPro Applet List"):
        super().__init__(module_name)
        self.isd = None
        self.app = []
        self.pkg = []
