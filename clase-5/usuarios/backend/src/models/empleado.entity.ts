import { Entity, Column, PrimaryGeneratedColumn } from 'typeorm';

@Entity('empleados')
export class EmpleadoEntity {
  @PrimaryGeneratedColumn()
  id!: number;

  @Column()
  nombre!: string;

  @Column()
  apellido!: string;

  @Column({ unique: true, nullable: true })
  email!: string;

  @Column({ unique: true, nullable: true })
  dni!: string;

  @Column({ nullable: true })
  telefono!: string;

  @Column({ nullable: true })
  direccion!: string;

  @Column({ nullable: true })
  departamento!: string;

  @Column({ nullable: true })
  cargo!: string;

  @Column({ default: 'activo' })
  estado!: string;

  @Column({ type: 'decimal', precision: 10, scale: 2, default: 0 })
  salario!: number;

  @Column({ type: 'timestamp', default: () => 'CURRENT_TIMESTAMP' })
  fechaContratacion!: Date;
}
