from terrascrape.core.component import Component


class CustomComponent(Component):
    @property
    def name(self):
        return 'custom_component'


def test_component_package_name():
    assert CustomComponent().package_name == 'tests.core.test_component'


def test_component_class_name():
    assert CustomComponent().class_name == 'CustomComponent'
