import unittest
import os
import tempfile
import shutil
from pathlib import Path
from unittest.mock import patch
import project_board_server

class TestProjectBoardServerRoot(unittest.TestCase):
    def setUp(self):
        self.old_cwd = os.getcwd()
        self.temp_dir = Path(tempfile.mkdtemp()).resolve()
        self.old_yaml_path = project_board_server.YAML_PATH
        self.old_artifacts_dir = project_board_server.ARTIFACTS_DIR
        self.old_planning_dir = project_board_server.PLANNING_DIR
        self.old_project_root = project_board_server.PROJECT_ROOT
        
    def tearDown(self):
        os.chdir(self.old_cwd)
        shutil.rmtree(self.temp_dir)
        project_board_server.YAML_PATH = self.old_yaml_path
        project_board_server.ARTIFACTS_DIR = self.old_artifacts_dir
        project_board_server.PLANNING_DIR = self.old_planning_dir
        project_board_server.PROJECT_ROOT = self.old_project_root

    def test_find_project_root_from_script_ancestry(self):
        # Create mock structure:
        # temp_dir/
        #   .agents/  (marker dir)
        #   nested1/
        #     nested2/
        (self.temp_dir / ".agents").mkdir()
        nested_dir = self.temp_dir / "nested1" / "nested2"
        nested_dir.mkdir(parents=True)
        
        # Patch __file__ of the server module to nested_dir / "project_board_server.py"
        mock_file = str(nested_dir / "project_board_server.py")
        with patch('project_board_server.__file__', mock_file):
            resolved = project_board_server.find_project_root()
            self.assertEqual(resolved.resolve(), self.temp_dir.resolve())

    def test_find_project_root_from_cwd_ancestry(self):
        # Create mock structure:
        # temp_dir/
        #   _bmad-output/  (marker dir)
        #   nested1/
        (self.temp_dir / "_bmad-output").mkdir()
        nested_dir = self.temp_dir / "nested1"
        nested_dir.mkdir(parents=True)
        
        # Patch __file__ to a fake path that doesn't exist and has no markers
        # so that script_dir walk-up returns None
        mock_file = "/nonexistent/path/project_board_server.py"
        with patch('project_board_server.__file__', mock_file):
            os.chdir(nested_dir)
            resolved = project_board_server.find_project_root()
            self.assertEqual(resolved.resolve(), self.temp_dir.resolve())

    def test_find_project_root_fallback_cwd(self):
        # No markers exist anywhere
        mock_file = "/nonexistent/path/project_board_server.py"
        with patch('project_board_server.__file__', mock_file):
            os.chdir(self.temp_dir)
            resolved = project_board_server.find_project_root()
            self.assertEqual(resolved.resolve(), self.temp_dir.resolve())

    @patch('builtins.print')
    @patch('project_board_server.HTTPServer')
    def test_main_cli_override(self, mock_http_server, mock_print):
        mock_server_instance = mock_http_server.return_value
        mock_server_instance.serve_forever.side_effect = KeyboardInterrupt()
        
        custom_path = self.temp_dir / "custom_project_root"
        custom_path.mkdir()
        
        with patch('sys.argv', ['project_board_server.py', '--project-root', str(custom_path), '--port', '9999']):
            project_board_server.main()
        
        self.assertEqual(project_board_server.PROJECT_ROOT, custom_path.resolve())
        self.assertEqual(project_board_server.YAML_PATH, custom_path.resolve() / "_bmad-output" / "implementation-artifacts" / "sprint-status.yaml")
        mock_http_server.assert_called_once_with(("localhost", 9999), project_board_server.ProjectBoardRequestHandler)

    @patch('sys.argv', ['project_board_server.py', '--port', '8012'])
    @patch('builtins.print')
    @patch('project_board_server.HTTPServer')
    @patch('project_board_server.find_project_root')
    def test_main_cli_default(self, mock_find_project_root, mock_http_server, mock_print):
        mock_find_project_root.return_value = Path('/mocked/default/root')
        mock_server_instance = mock_http_server.return_value
        mock_server_instance.serve_forever.side_effect = KeyboardInterrupt()
        
        project_board_server.main()
        
        self.assertEqual(project_board_server.PROJECT_ROOT, Path('/mocked/default/root'))
        mock_http_server.assert_called_once_with(("localhost", 8012), project_board_server.ProjectBoardRequestHandler)

    @patch('sys.stderr')
    def test_main_cli_invalid_port(self, mock_stderr):
        with patch('sys.argv', ['project_board_server.py', '--port', '70000']):
            with self.assertRaises(SystemExit):
                project_board_server.main()

    @patch('sys.stderr')
    def test_main_cli_nonexistent_root(self, mock_stderr):
        nonexistent = self.temp_dir / "does_not_exist"
        with patch('sys.argv', ['project_board_server.py', '--project-root', str(nonexistent)]):
            with self.assertRaises(SystemExit):
                project_board_server.main()

    @patch('sys.stderr')
    def test_main_cli_root_not_dir(self, mock_stderr):
        file_path = self.temp_dir / "some_file.txt"
        file_path.write_text("hello")
        with patch('sys.argv', ['project_board_server.py', '--project-root', str(file_path)]):
            with self.assertRaises(SystemExit):
                project_board_server.main()

    def test_load_project_config_found(self):
        bmad_dir = self.temp_dir / "_bmad" / "bmm"
        bmad_dir.mkdir(parents=True)
        config_file = bmad_dir / "config.yaml"
        config_file.write_text("implementation_artifacts_dir: custom-impl\nplanning_artifacts_dir: \"custom-plan\"")
        
        config = project_board_server.load_project_config(self.temp_dir)
        self.assertEqual(config.get("implementation_artifacts_dir"), "custom-impl")
        self.assertEqual(config.get("planning_artifacts_dir"), "custom-plan")

    def test_load_project_config_not_found(self):
        config = project_board_server.load_project_config(self.temp_dir)
        self.assertEqual(config, {})

    def test_get_prd_content_found(self):
        project_board_server.PROJECT_ROOT = self.temp_dir
        project_board_server.PLANNING_DIR = self.temp_dir / "planning"
        project_board_server.PLANNING_DIR.mkdir()
        
        prd_file = project_board_server.PLANNING_DIR / "prd.md"
        prd_file.write_text("Hello PRD")
        
        name, content = project_board_server.get_prd_content()
        self.assertEqual(name, "prd.md")
        self.assertEqual(content, "Hello PRD")

    def test_get_prd_content_not_found(self):
        project_board_server.PROJECT_ROOT = self.temp_dir
        project_board_server.PLANNING_DIR = self.temp_dir / "planning"
        
        name, content = project_board_server.get_prd_content()
        self.assertEqual(name, "PRD Not Found")

if __name__ == "__main__":
    unittest.main()
