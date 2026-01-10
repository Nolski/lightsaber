#!/usr/bin/env python3
"""
Lightsaber CLI - Interactive Ansible workflow runner
An interactive command-line utility to run various Ansible playbooks and roles.
"""

import os
import sys
import json
import subprocess
import argparse
from pathlib import Path
from typing import List, Dict, Optional

# Project root directory - resolve symlinks to get actual script location
_script_path = os.path.realpath(__file__)
PROJECT_ROOT = Path(_script_path).parent.parent.resolve()
INVENTORY_FILE = PROJECT_ROOT / "inventory" / "inventory"
PLAYBOOKS_DIR = PROJECT_ROOT / "playbooks"


class Colors:
    """ANSI color codes for terminal output"""
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def print_header(text: str):
    """Print a formatted header"""
    print(f"\n{Colors.BOLD}{Colors.HEADER}{'=' * 60}{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.HEADER}{text.center(60)}{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.HEADER}{'=' * 60}{Colors.ENDC}\n")


def print_success(text: str):
    """Print success message"""
    print(f"{Colors.OKGREEN}✓{Colors.ENDC} {text}")


def print_error(text: str):
    """Print error message"""
    print(f"{Colors.FAIL}✗{Colors.ENDC} {text}")


def print_info(text: str):
    """Print info message"""
    print(f"{Colors.OKCYAN}ℹ{Colors.ENDC} {text}")


def print_menu(items: List[tuple], title: Optional[str] = None):
    """Print a menu and return selected item"""
    if title:
        print(f"\n{Colors.BOLD}{title}{Colors.ENDC}")
    
    for i, (key, description) in enumerate(items, 1):
        print(f"  {Colors.OKBLUE}{i}{Colors.ENDC}. {description}")
    
    print(f"  {Colors.OKBLUE}0{Colors.ENDC}. Exit")
    
    while True:
        try:
            choice = input(f"\n{Colors.BOLD}Select option{Colors.ENDC} (0-{len(items)}): ").strip()
            if choice == '0':
                return None
            idx = int(choice) - 1
            if 0 <= idx < len(items):
                return items[idx][0]
            else:
                print_error(f"Invalid choice. Please enter a number between 0 and {len(items)}")
        except (ValueError, KeyboardInterrupt):
            print_error("Invalid input. Please enter a number.")
            if choice == '':
                continue
        except EOFError:
            print("\n")
            return None


def get_playbooks() -> List[Dict[str, str]]:
    """Get list of available playbooks"""
    playbooks = []
    
    # Main playbooks
    main_playbook = PLAYBOOKS_DIR / "fedora-workstation.yml"
    if main_playbook.exists():
        playbooks.append({
            'name': 'fedora-workstation',
            'path': str(main_playbook.relative_to(PROJECT_ROOT)),
            'description': 'Fedora Workstation Setup (main)'
        })
    
    # Host-specific playbooks
    hosts_dir = PLAYBOOKS_DIR / "hosts"
    if hosts_dir.exists():
        for playbook in hosts_dir.glob("*.yml"):
            host_name = playbook.stem
            playbooks.append({
                'name': f'hosts/{host_name}',
                'path': str(playbook.relative_to(PROJECT_ROOT)),
                'description': f'Host-specific: {host_name}'
            })
    
    return playbooks


def get_tags_from_playbook(playbook_path: Path) -> List[str]:
    """Extract tags from a playbook file"""
    tags = set()
    try:
        with open(playbook_path, 'r') as f:
            content = f.read()
            # Simple tag extraction (look for tags: ['tag1', 'tag2'])
            import re
            tag_pattern = r"tags:\s*\[(.*?)\]"
            for match in re.finditer(tag_pattern, content):
                tag_list = match.group(1)
                for tag in re.findall(r"'([^']+)'|\"([^\"]+)\"", tag_list):
                    tags.add(tag[0] or tag[1])
    except Exception as e:
        print_error(f"Could not parse tags from playbook: {e}")
    
    return sorted(list(tags))


def run_ansible_playbook(playbook: str, tags: Optional[List[str]] = None, 
                        check_mode: bool = False, verbose: int = 0,
                        limit: Optional[str] = None, ask_become_pass: bool = True):
    """Run an Ansible playbook with specified options"""
    # #region agent log
    log_path = '/home/nolski/code/lightsaber/.cursor/debug.log'
    os.makedirs(os.path.dirname(log_path), exist_ok=True)
    with open(log_path, 'a') as f:
        import time
        f.write(json.dumps({
            'location': 'lightsaber-cli.py:131',
            'message': 'run_ansible_playbook called',
            'data': {
                'playbook': playbook,
                'check_mode': check_mode,
                'ask_become_pass': ask_become_pass,
                'tags': tags,
                'verbose': verbose
            },
            'timestamp': int(time.time() * 1000),
            'sessionId': 'debug-session',
            'runId': 'run1',
            'hypothesisId': 'A'
        }) + '\n')
    # #endregion
    
    cmd = ['ansible-playbook', '-i', str(INVENTORY_FILE)]
    
    # Always use privilege escalation (become)
    cmd.append('--become')
    
    if ask_become_pass:
        cmd.append('--ask-become-pass')
    
    if check_mode:
        cmd.append('--check')
    
    if verbose > 0:
        cmd.append('-' + 'v' * min(verbose, 4))
    
    if tags:
        cmd.extend(['--tags', ','.join(tags)])
    
    if limit:
        cmd.extend(['--limit', limit])
    
    cmd.append(playbook)
    
    # #region agent log
    log_path = '/home/nolski/code/lightsaber/.cursor/debug.log'
    os.makedirs(os.path.dirname(log_path), exist_ok=True)
    with open(log_path, 'a') as f:
        import time
        f.write(json.dumps({
            'location': 'lightsaber-cli.py:157',
            'message': 'Command built',
            'data': {
                'cmd': ' '.join(cmd),
                'has_become': '--become' in cmd,
                'has_ask_become_pass': '--ask-become-pass' in cmd,
                'has_check': '--check' in cmd
            },
            'timestamp': int(time.time() * 1000),
            'sessionId': 'debug-session',
            'runId': 'run1',
            'hypothesisId': 'A'
        }) + '\n')
    # #endregion
    
    print_info(f"Running: {' '.join(cmd)}")
    print()
    
    try:
        result = subprocess.run(cmd, cwd=PROJECT_ROOT)
        return result.returncode == 0
    except KeyboardInterrupt:
        print_error("\nExecution cancelled by user")
        return False
    except FileNotFoundError:
        print_error("ansible-playbook not found. Please install Ansible.")
        return False


def interactive_mode():
    """Interactive menu-driven mode"""
    print_header("Lightsaber CLI - Ansible Workflow Runner")
    
    while True:
        # Main menu
        menu_items = [
            ('run_playbook', 'Run a Playbook'),
            ('run_tags', 'Run Specific Tags'),
            ('check_mode', 'Dry Run (Check Mode)'),
            ('list_playbooks', 'List Available Playbooks'),
            ('list_tags', 'List Available Tags'),
        ]
        
        choice = print_menu(menu_items, "Main Menu")
        
        if choice is None:
            print_info("Goodbye!")
            break
        elif choice == 'list_playbooks':
            playbooks = get_playbooks()
            print_header("Available Playbooks")
            for pb in playbooks:
                print(f"  • {Colors.OKCYAN}{pb['name']}{Colors.ENDC}: {pb['description']}")
        elif choice == 'list_tags':
            playbooks = get_playbooks()
            if not playbooks:
                print_error("No playbooks found")
                continue
            
            pb_items = [(pb['name'], pb['description']) for pb in playbooks]
            selected_pb = print_menu(pb_items, "Select Playbook to View Tags")
            if selected_pb:
                pb_path = PROJECT_ROOT / next(pb['path'] for pb in playbooks if pb['name'] == selected_pb)
                tags = get_tags_from_playbook(pb_path)
                print_header(f"Available Tags for {selected_pb}")
                for tag in tags:
                    print(f"  • {Colors.OKCYAN}{tag}{Colors.ENDC}")
        elif choice == 'run_playbook':
            playbooks = get_playbooks()
            if not playbooks:
                print_error("No playbooks found")
                continue
            
            pb_items = [(pb['name'], pb['description']) for pb in playbooks]
            selected_pb = print_menu(pb_items, "Select Playbook to Run")
            if selected_pb:
                pb_path = str(PROJECT_ROOT / next(pb['path'] for pb in playbooks if pb['name'] == selected_pb))
                
                # Ask for options
                check = input(f"\n{Colors.WARNING}Run in check mode (dry run)? [y/N]: {Colors.ENDC}").strip().lower() == 'y'
                verbose_input = input(f"{Colors.WARNING}Verbosity level (0-4, default 1): {Colors.ENDC}").strip()
                verbose = int(verbose_input) if verbose_input.isdigit() and 0 <= int(verbose_input) <= 4 else 1
                
                ask_pass = input(f"{Colors.WARNING}Ask for sudo password? [Y/n]: {Colors.ENDC}").strip().lower()
                ask_become = ask_pass != 'n'
                
                success = run_ansible_playbook(pb_path, check_mode=check, verbose=verbose, ask_become_pass=ask_become)
                
                if success:
                    print_success("Playbook execution completed successfully!")
                else:
                    print_error("Playbook execution failed!")
        elif choice == 'run_tags':
            playbooks = get_playbooks()
            if not playbooks:
                print_error("No playbooks found")
                continue
            
            pb_items = [(pb['name'], pb['description']) for pb in playbooks]
            selected_pb = print_menu(pb_items, "Select Playbook")
            if selected_pb:
                pb_path = PROJECT_ROOT / next(pb['path'] for pb in playbooks if pb['name'] == selected_pb)
                tags = get_tags_from_playbook(pb_path)
                
                if not tags:
                    print_error("No tags found in playbook")
                    continue
                
                tag_items = [(tag, tag) for tag in tags]
                selected_tags = []
                print_info("Select tags to run (multiple selections, 'done' to finish):")
                
                while True:
                    tag_choice = print_menu(tag_items + [('done', 'Done selecting tags')], "Select Tags")
                    if tag_choice == 'done' or tag_choice is None:
                        break
                    if tag_choice not in selected_tags:
                        selected_tags.append(tag_choice)
                        print_success(f"Added tag: {tag_choice}")
                    else:
                        print_info(f"Tag {tag_choice} already selected")
                
                if selected_tags:
                    check = input(f"\n{Colors.WARNING}Run in check mode (dry run)? [y/N]: {Colors.ENDC}").strip().lower() == 'y'
                    verbose_input = input(f"{Colors.WARNING}Verbosity level (0-4, default 1): {Colors.ENDC}").strip()
                    verbose = int(verbose_input) if verbose_input.isdigit() and 0 <= int(verbose_input) <= 4 else 1
                    
                    ask_pass = input(f"{Colors.WARNING}Ask for sudo password? [Y/n]: {Colors.ENDC}").strip().lower()
                    ask_become = ask_pass != 'n'
                    
                    pb_file = str(pb_path)
                    success = run_ansible_playbook(pb_file, tags=selected_tags, check_mode=check, 
                                                 verbose=verbose, ask_become_pass=ask_become)
                    
                    if success:
                        print_success("Tag execution completed successfully!")
                    else:
                        print_error("Tag execution failed!")
        elif choice == 'check_mode':
            playbooks = get_playbooks()
            if not playbooks:
                print_error("No playbooks found")
                continue
            
            pb_items = [(pb['name'], pb['description']) for pb in playbooks]
            selected_pb = print_menu(pb_items, "Select Playbook for Dry Run")
            if selected_pb:
                pb_path = str(PROJECT_ROOT / next(pb['path'] for pb in playbooks if pb['name'] == selected_pb))
                print_info("Running in check mode (dry run - no changes will be made)")
                
                # Ask for sudo password - even in check mode, fact gathering requires sudo when become: yes is set
                ask_pass = input(f"{Colors.WARNING}Ask for sudo password? [Y/n]: {Colors.ENDC}").strip().lower()
                ask_become = ask_pass != 'n'
                
                # #region agent log
                log_path = '/home/nolski/code/lightsaber/.cursor/debug.log'
                os.makedirs(os.path.dirname(log_path), exist_ok=True)
                with open(log_path, 'a') as f:
                    import time
                    f.write(json.dumps({
                        'location': 'lightsaber-cli.py:292',
                        'message': 'check_mode menu option calling run_ansible_playbook',
                        'data': {
                            'playbook': pb_path,
                            'ask_become_pass': ask_become,
                            'check_mode': True,
                            'user_input': ask_pass
                        },
                        'timestamp': int(time.time() * 1000),
                        'sessionId': 'debug-session',
                        'runId': 'run1',
                        'hypothesisId': 'A'
                    }) + '\n')
                # #endregion
                
                success = run_ansible_playbook(pb_path, check_mode=True, verbose=1, ask_become_pass=ask_become)
                
                if success:
                    print_success("Check mode completed successfully!")
                else:
                    print_error("Check mode failed!")


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='Lightsaber CLI - Interactive Ansible workflow runner',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                    # Interactive mode
  %(prog)s --playbook fedora-workstation.yml --check
  %(prog)s --playbook fedora-workstation.yml --tags powerline,cursor
        """
    )
    
    parser.add_argument('--playbook', '-p', 
                       help='Playbook to run (non-interactive mode)')
    parser.add_argument('--tags', '-t',
                       help='Comma-separated list of tags to run')
    parser.add_argument('--check', '-C', action='store_true',
                       help='Run in check mode (dry run)')
    parser.add_argument('--verbose', '-v', action='count', default=0,
                       help='Verbose output (use -v, -vv, -vvv, or -vvvv)')
    parser.add_argument('--limit', '-l',
                       help='Limit execution to specific hosts')
    parser.add_argument('--no-ask-pass', action='store_true',
                       help='Do not ask for sudo password')
    parser.add_argument('--list-playbooks', action='store_true',
                       help='List available playbooks and exit')
    parser.add_argument('--list-tags', metavar='PLAYBOOK',
                       help='List available tags for a playbook and exit')
    
    args = parser.parse_args()
    
    # Handle list commands
    if args.list_playbooks:
        playbooks = get_playbooks()
        print_header("Available Playbooks")
        for pb in playbooks:
            print(f"  {Colors.OKCYAN}{pb['path']}{Colors.ENDC}")
            print(f"    Description: {pb['description']}\n")
        return 0
    
    if args.list_tags:
        pb_path = PROJECT_ROOT / args.list_tags
        if not pb_path.exists():
            pb_path = PLAYBOOKS_DIR / args.list_tags
        if not pb_path.exists():
            print_error(f"Playbook not found: {args.list_tags}")
            return 1
        
        tags = get_tags_from_playbook(pb_path)
        print_header(f"Available Tags: {args.list_tags}")
        for tag in tags:
            print(f"  • {Colors.OKCYAN}{tag}{Colors.ENDC}")
        return 0
    
    # Non-interactive mode
    if args.playbook:
        tags = args.tags.split(',') if args.tags else None
        pb_path = PROJECT_ROOT / args.playbook
        if not pb_path.exists():
            pb_path = PLAYBOOKS_DIR / args.playbook
        if not pb_path.exists():
            print_error(f"Playbook not found: {args.playbook}")
            return 1
        
        success = run_ansible_playbook(
            str(pb_path),
            tags=tags,
            check_mode=args.check,
            verbose=args.verbose,
            limit=args.limit,
            ask_become_pass=not args.no_ask_pass
        )
        return 0 if success else 1
    
    # Interactive mode
    try:
        interactive_mode()
    except KeyboardInterrupt:
        print("\n\n")
        print_info("Interrupted by user. Goodbye!")
        return 130
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
