import Link from 'next/link'
import styles from '@/styles/Layout.module.css'

export default function Layout({ children }) {
  return (
    <div className={styles.container}>
      <nav className={styles.navbar}>
        <div className={styles.navBrand}>Shot Selector</div>
        <div className={styles.navLinks}>
          <Link href="/" className={styles.navLink}>Home</Link>
          <Link href="/analyze" className={styles.navLink}>Analyze Prompt</Link>
        </div>
      </nav>

      <main className={styles.main}>
        {children}
      </main>

      <footer className={styles.footer}>
        <p>&copy; 2024 Shot Selector. All rights reserved.</p>
      </footer>
    </div>
  )
} 